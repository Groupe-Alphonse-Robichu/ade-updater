
from icalendar.utils.parser import CalendarObject


class BaseNotifier :

	def missingTranslation(self, channel, group_name, summaries) :
		raise NotImplementedError

	def discovered(self, channel, cal_name, event_counts) :
		raise NotImplementedError
	
	def weekSchedule(self, channel, cal_name, events: "list[CalendarObject]") :
		raise NotImplementedError
	
	def changes(self, channel, cal_name, insertions, deletions, modifications) :
		raise NotImplementedError
