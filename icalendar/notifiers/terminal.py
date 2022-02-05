
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.table import printTable
from icalendar.utils.parser import CalendarObject
from icalendar.utils.date import formatDatetime, formatTimedelta

import logging

logger = logging.getLogger(__name__)


class TerminalNotifier(BaseNotifier) :

	def missingTranslation(self, group: GroupConf, summaries) :
		# printTable([[e] for e in summaries], f"Missing translations in {group_name}")
		logger.warning(f"NOT_FOUND total {len(summaries)} missing translation{'s' if len(summaries) > 0 else ''} in group {group.getName()}")
	
	def archive(self, group: GroupConf) :
		pass

	def discovered(self, cal: CalendarConf, event_counts: dict, begin, end) :
		columns = ['Event', 'Count', 'Duration']
		ll = [(evt, c[0], formatTimedelta(c[1])) for evt, c in event_counts.items()]
		total_nb = 0
		total_time = 0.0
		for c in event_counts.values() :
			total_nb += c[0]
			total_time += c[1]
		ll.insert(0, columns)
		ll.append(('Total', total_nb, formatTimedelta(total_time)))
		printTable(ll, cal.getFullName())
	
	def weekSchedule(self, cal: CalendarConf, ical: CalendarObject) :
		columns = ['Time', 'Event', 'Location']
		ll = [
			(
				formatDatetime(evt.getProperty('DTSTART')),
				evt.getProperty('SUMMARY'),
				evt.getPropertyOrDefault('LOCATION')
			) for evt in ical.getObjects()
		]
		ll.insert(0, columns)
		printTable(ll, f"{cal.getFullName()} - week {cal.getWeek()}")
	
	def changes(self, cal: CalendarConf, insertions, deletions, modifications) :
		logger.info(f"TOTAL {len(insertions)} additions, {len(deletions)} deletions, {len(modifications)} modifications")
