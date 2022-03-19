
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

def formatRole(role_id) :
	return f"<@&{role_id}>"

def formatDate(dt: IcalDate) -> str :
	return f"<t:{dt.getTimestamp()}:d>"

def formatLongDate(dt: IcalDate) -> str :
	return f"<t:{dt.getTimestamp()}:D>"

def formatTime(dt: IcalDate) -> str :
	return f"<t:{dt.getTimestamp()}:t>"

def formatTimeRange(evt) :
	dt1 = IcalDate(evt[0])
	dt2 = IcalDate(evt[1])
	date = formatDate(dt1)
	time1 = formatTime(dt1)
	time2 = formatTime(dt2)
	# date, time1 = IcalDate(evt[0]).fixTimezone().splitDatetime()
	# time2 = IcalDate(evt[1]).fixTimezone().formatTime()
	return date, f"{time1} - {time2}"

# The notifier may start to spam Discord servers a little when there are a lot of calendars.
# Maybe add a delay betwenn each request ?

class DiscordNotifier(BaseNotifier) :

	def missingTranslation(self, group: GroupConf, summaries: "list[str]") :
		if len(summaries) == 0 :
			return
		if group.getAlertChannel() is None :
			logger.warning(f"UNDEFINED alert channel for group {group.getName()}")
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
		if group.getAlertChannel() is None :
			logger.warning(f"UNDEFINED alert channel for group {group.getName()}")
			return
		webhook = DiscordWebhook(url=group.getAlertChannel(), content=f"Calendar group {group.getName()} has reached its limit date and will no longer be updated.")
		webhook.execute()
	
	def weekSchedule(self, cal: CalendarConf, ical: CalendarObject, startOfWeek: AdeDate) :
		if not ical.hasObjects() :
			return
		if cal.getNotify() is None :
			logger.warning(f"UNDEFINED alert channel for calendar {cal.getFullName()}")
			return
		message = f"Voici l'emploi du temps de la semaine du {startOfWeek.format()}"
		webhook = DiscordWebhook(url=cal.getNotify(), content=message)
		days = {}
		for obj in ical :
			startDate = IcalDate(obj.getProperty('DTSTART'))
			date = startDate.getDate()
			if date not in days : 
				days[date] = formatLongDate(startDate), []
			days[date][1].append((
				obj.getProperty('SUMMARY'),
				formatTime(startDate),
				formatTime(IcalDate(obj.getProperty('DTEND'))),
				obj.getPropertyOrDefault('LOCATION')
			))
		for date, events in days.values() :
			embed = DiscordEmbed(title=date, color='9b40e6')
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

	def _recent_modifications(self, insertions: list, deletions: list, modifications: list) -> bool :
		now = IcalDate.today().format()
		for evt_list in [insertions, deletions, [evt for _, evt in modifications]] :
			for evt in evt_list :
				if now < evt[0] :
					return True
		return False
		
	def changes(self, cal: CalendarConf, insertions: list, deletions: list, modifications: list) :
		if cal.getNotify() is None :
			logger.warning(f"UNDEFINED alert channel for calendar {cal.getFullName()}")
			return
		edits = {
			'Nouveaux cours': ('3bf573', insertions),
			'Cours supprimés': ('f53b3b', deletions)
		}
		webhook = DiscordWebhook(url=cal.getNotify())
		message = f"Des modifications ont été détectées depuis le {AdeDate.fromString(cal.getUpdate()).format()}"
		role_id = cal.getRoleId()
		if role_id is not None and self._recent_modifications(insertions, deletions, modifications):
			message += " " + formatRole(role_id)
			webhook.allowed_mentions={'roles': [str(role_id)]}
		webhook.content=message
		for title, content in edits.items() :
			evt_states = content[1]
			if len(evt_states) > 0 :
				embed = DiscordEmbed(title=title, color=content[0])
				for evt in evt_states :
					date, time = formatTimeRange(evt)
					desc = f"{date}, {time}"
					if len(evt[3]) > 0 :
						desc += f"\n{evt[3]}"
					embed.add_embed_field(name=evt[2], value=desc)
				embed.set_footer(text=PROJECT_URL)
				embed.set_timestamp()
				webhook.add_embed(embed)
		if len(modifications) > 0 :
			embed = DiscordEmbed(title='Cours modifiés', color='3b9bf5')
			for old_state, new_state in modifications :
				title = f"~~{old_state[2]}~~ -> **{new_state[2]}**" if old_state[2] != new_state[2] else old_state[2]
				d1, t1 = formatTimeRange(old_state)
				d2, t2 = formatTimeRange(new_state)
				date = f"~~{d1}~~ -> **{d2}**" if d1 != d2 else d1
				time = f"~~{t1}~~ -> **{t2}**" if t1 != t2 else t1
				desc = f"{date}\n{time}"
				if old_state[3] != '' or new_state[3] != '' :
					desc += "\n"
					if old_state[3] != new_state[3] :
						if old_state[3] == '' :
							desc += f"**{new_state[3]}**"
						elif new_state[3] == '' :
							desc += f"~~{old_state[3]}~~"
						else :
							desc += f"~~{old_state[3]}~~ -> **{new_state[3]}**"
					else :
						desc += old_state[3]
				embed.add_embed_field(name=title, value=desc)
			embed.set_footer(text=PROJECT_URL)
			embed.set_timestamp()
			webhook.add_embed(embed)
		response = webhook.execute()
		if response.ok :
			logger.info(f"WEBHOOK posted for calendar {cal.getFullName()}")
		else :
			logger.info(f"WEBHOOK failed for calendar {cal.getFullName()} with status code {response.status_code}")
	
