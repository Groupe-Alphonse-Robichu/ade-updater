
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf
from icalendar.utils.date import AdeDate, formatTimedelta
from icalendar.utils.parser import CalendarObject
from icalendar.utils.table import printTable


class BaseNotifier :

	def missingTranslation(self, group: GroupConf, summaries) :
		raise NotImplementedError

	def archive(self, group: GroupConf) :
		raise NotImplementedError

	def discovered(self, cal: CalendarConf, event_counts: dict, begin: AdeDate, end: AdeDate) :
		columns = ['Event', 'Count', 'Duration']
		ll = [(evt, c[0], formatTimedelta(c[1])) for evt, c in event_counts.items()]
		total_nb = 0
		total_time = 0.0
		for c in event_counts.values() :
			total_nb += c[0]
			total_time += c[1]
		ll.insert(0, columns)
		ll.append(('Total', total_nb, formatTimedelta(total_time)))
		printTable(ll, f"{cal.getFullName()} {begin.format()} - {end.format()}")
	
	def weekSchedule(self, cal: CalendarConf, ical: CalendarObject, startOfWeek: AdeDate) :
		raise NotImplementedError
	
	def changes(self, cal: CalendarConf, insertions, deletions, modifications) :
		raise NotImplementedError
