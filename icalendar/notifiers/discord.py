
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.parser import CalendarObject


class DiscordNotifier(BaseNotifier) :

	def missingTranslation(self, group: GroupConf, summaries) :
		raise NotImplementedError
	
	def archive(self, group: GroupConf) :
		raise NotImplementedError

	def discovered(self, cal: CalendarConf, event_counts, begin, end) :
		raise NotImplementedError
	
	def weekSchedule(self, cal: CalendarConf, ical: CalendarObject) :
		raise NotImplementedError
	
	def changes(self, cal: CalendarConf, insertions, deletions, modifications) :
		raise NotImplementedError
	
