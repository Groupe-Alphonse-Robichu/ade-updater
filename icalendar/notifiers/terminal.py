
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.table import printTable
from icalendar.utils.parser import CalendarObject
from icalendar.utils.date import AdeDate, IcalDate

import logging

logger = logging.getLogger(__name__)


class TerminalNotifier(BaseNotifier) :

	def missingTranslation(self, group: GroupConf, summaries) :
		# printTable([[e] for e in summaries], f"Missing translations in {group_name}")
		logger.warning(f"NOT_FOUND total {len(summaries)} missing translation{'s' if len(summaries) > 0 else ''} in group {group.getName()}")
	
	def archive(self, group: GroupConf) :
		pass
	
	def weekSchedule(self, cal: CalendarConf, ical: CalendarObject, startOfWeek: AdeDate) :
		columns = ['Time', 'Event', 'Location']
		ll = [
			(
				str(IcalDate(evt.getProperty('DTSTART'))),
				evt.getProperty('SUMMARY'),
				evt.getPropertyOrDefault('LOCATION')
			) for evt in ical
		]
		ll.insert(0, columns)
		printTable(ll, f"{cal.getFullName()} - week {cal.getWeek()}")
	
	def changes(self, cal: CalendarConf, insertions, deletions, modifications) :
		logger.info(f"TOTAL {len(insertions)} additions, {len(deletions)} deletions, {len(modifications)} modifications")
