
from icalendar.utils.date import AdeDate
from icalendar.utils.parser import CalendarObject


class CalendarSource :

	def getURL(self, begin: AdeDate, end: AdeDate) -> str :
		raise NotImplementedError('Subtypes of CalendarSource must implement the getURL method')

	def processEvent(self, event: CalendarObject) -> "CalendarObject | None" :
		return event