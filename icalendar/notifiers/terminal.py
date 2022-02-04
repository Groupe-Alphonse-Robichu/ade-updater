
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.table import printTable
from icalendar.utils.parser import CalendarObject
from icalendar.utils.date import formatDatetime, formatTimedelta

import logging

logger = logging.getLogger(__name__)


class TerminalNotifier(BaseNotifier) :

	def missingTranslation(self, _channel, group_name, summaries) :
		# printTable([[e] for e in summaries], f"Missing translations in {group_name}")
		logger.warning(f"NOT_FOUND total {len(summaries)} missing translation{'s' if len(summaries) > 0 else ''} in group {group_name}")

	def discovered(self, _channel, cal_name, event_counts) :
		columns = ['Event', 'Count', 'Duration']
		ll = [(evt, c[0], formatTimedelta(c[1])) for evt, c in event_counts.items()]
		ll.insert(0, columns)
		printTable(ll, cal_name)
	
	def weekSchedule(self, _channel, cal_name, week, ical: CalendarObject) :
		columns = ['Time', 'Event', 'Location']
		ll = [
			(
				evt.getProperty('SUMMARY'),
				formatDatetime(evt.getProperty('DTSTART')),
				evt.getPropertyOrDefault('LOCATION')
			) for evt in ical.getObjects()
		]
		ll.insert(0, columns)
		printTable(ll, f"{cal_name} - week {week}")
	
	def changes(self, _channel, cal_name, insertions, deletions, modifications) :
		logger.info(f"TOTAL {len(insertions)} additions, {len(deletions)} deletions, {len(modifications)} modifications")
