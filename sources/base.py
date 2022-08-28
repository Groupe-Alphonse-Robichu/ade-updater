
from icalendar.utils.parser import CalendarObject

from datetime import date


class CalendarSource :

	def getURL(self, begin: date, end: date) -> str :
		raise NotImplementedError('Subtypes of CalendarSource must implement the getURL method')

	def processEvent(self, event: CalendarObject) -> CalendarObject :
		return event