
from importlib.resources import contents
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.date import AdeDate, IcalDate
from icalendar.utils.parser import CalendarObject

import logging
from collections import deque
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import Response

logger = logging.getLogger(__name__)

PROJECT_URL = "https://github.com/Groupe-Alphonse-Robichu/ade-updater"

# The notifier may start to spam Discord servers a little when there are a lot of calendars.
# Maybe add a delay betwenn each request ?

class DiscordNotifier(BaseNotifier) :

	def missingTranslation(self, group: GroupConf, summaries: "list[str]") :
		if len(summaries) == 0 :
			return
		summ = deque(summaries)
		message = 'The translations for the following events were not found : \n```\n'
		while len(summ) > 0 :
			while len(summ) > 0 and len(message) + len(summ[0]) < 1995 :
				message += summ.popleft() + "\n"
			message += "```"
			webhook = DiscordWebhook(url=group.getAlertChannel(), content=message)
			webhook.execute()
			message = '```\n'
	
	def archive(self, group: GroupConf) :
		webhook = DiscordWebhook(url=group.getAlertChannel(), content=f"Calendar group {group.getName()} has reached its limit date and will no longer be updated.")
		webhook.execute()
	
	def weekSchedule(self, cal: CalendarConf, ical: CalendarObject, startOfWeek: AdeDate) :
		if not ical.hasObjects() :
			return
		message = f"Voici l'emploi du temps de la semaine du {startOfWeek.format()}"
		webhook = DiscordWebhook(url=cal.getNotify(), content=message)
		days = {}
		for obj in ical :
			startDate = IcalDate(obj.getProperty('DTSTART'))
			date, time = startDate.splitDatetime()
			if date not in days : 
				days[date] = []
			days[date].append((
				obj.getProperty('SUMMARY'),
				time,
				IcalDate(obj.getProperty('DTEND')).formatTime(),
				obj.getPropertyOrDefault('LOCATION')
			))
		for day, events in days.items() :
			embed = DiscordEmbed(title=day, color='9b40e6')
			for evt in events :
				desc = f"{evt[1]} - {evt[2]}" + (f"\n{evt[3]}" if len(evt[3]) > 0 else "")
				embed.add_embed_field(name=evt[0], value=desc)
			embed.set_footer(text=PROJECT_URL)
			embed.set_timestamp()
			webhook.add_embed(embed)
		response: Response = webhook.execute()
		if response.ok :
			logger.info(f"WEBHOOK posted for calendar {cal.getFullName()}")
		else :
			logger.info(f"WEBHOOK failed for calendar {cal.getFullName()} with status code {response.status_code}")

	
	def changes(self, cal: CalendarConf, insertions: list, deletions: list, modifications: list) :
		edits = {
			"Nouveaux cours": ('3bf573', insertions),
			"Cours supprimés": ('f53b3b', deletions),
			"Cours modifiés": ('3b9bf5', [m[1] for m in modifications])
		}
		message = f"Des modifications ont été détectées depuis le {AdeDate.fromString(cal.getUpdate()).format()}"
		webhook = DiscordWebhook(url=cal.getNotify(), content=message)
		for title, content in edits.items() :
			evt_states = content[1]
			if len(evt_states) > 0 :
				embed = DiscordEmbed(title=title, color=content[0])
				for evt in evt_states :
					date, time1 = IcalDate(evt[0]).splitDatetime()
					time2 = IcalDate(evt[1]).formatTime()
					desc = f"{date}, {time1} - {time2}" + (f"\n{evt[3]}" if len(evt[3]) > 0 else "")
					embed.add_embed_field(name=evt[2], value=desc)
				embed.set_footer(text=PROJECT_URL)
				embed.set_timestamp()
				webhook.add_embed(embed)
		response = webhook.execute()
		if response.ok :
			logger.info(f"WEBHOOK posted for calendar {cal.getFullName()}")
		else :
			logger.info(f"WEBHOOK failed for calendar {cal.getFullName()} with status code {response.status_code}")
	
