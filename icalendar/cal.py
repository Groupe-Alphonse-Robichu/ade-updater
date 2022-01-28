from icalendar import SOURCES
from icalendar.translate import filterAndTranslate
from icalendar.utils.parser import CalendarObject
from icalendar.utils.date import AdeDate, currentWeek


class CalendarConf :

	def __init__(self, cal_name, group_name, group) :
		self._name = cal_name
		self._fullname = f"{group['source']}_{group_name}_{cal_name}"
		self._group_name = group_name
		self._group = group
		self._cal = group['calendars'][cal_name]
		self._url_template = SOURCES[group['source']]

	def _getUrl(self, start, end) -> str :
		url_data = {
			'start': start,
			'end': end,
			'project': self._group['project_id'],
			'resources': ",".join([str(i) for i in {*self._group['resources'], *self._cal['resources']}])
		}
		return self._url_template.substitute(url_data)
	
	def fetchIcal(self, start, end) -> "tuple[CalendarObject, list[str]]" :
		ical = CalendarObject.fromUrl(self._getUrl(start, end))
		no_translate = filterAndTranslate(self._fullname, self._group, ical)
		return ical, no_translate
	
	def getStart(self) -> str:
		return self._group['start']
	
	def getEnd(self) -> str :
		end = self._group['limit']
		return end if end is not None else str(AdeDate.fromString(self._group['start']).addDays(180))
	
	def getNotify(self) -> str :
		return self._cal['notify']
	
	def weekChanged(self, delta=0) -> bool :
		week = currentWeek(delta)
		return self._cal['week'] != week

	def setWeek(self, delta=0) :
		self._cal['week'] = currentWeek(delta)
	
	def setUpdate(self) :
		self._cal['update'] = str(AdeDate.today())
	
	def getFullName(self) :
		return self._fullname
