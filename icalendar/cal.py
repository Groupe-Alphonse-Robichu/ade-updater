from icalendar import SOURCES
from icalendar.translate import filterAndTranslate
from icalendar.utils.parser import CalendarObject
from icalendar.utils.date import AdeDate, currentWeek

import os


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
			'start': str(start),
			'end': str(end),
			'project': self._group['project_id'],
			'resources': ",".join([str(i) for i in {*self._group['resources'], *self._cal['resources']}])
		}
		return self._url_template.substitute(url_data)
	
	def fetchIcal(self, start, end) -> "tuple[CalendarObject, list[str]]" :
		ical = CalendarObject.fromUrl(self._getUrl(start, end))
		no_translate = filterAndTranslate(self._fullname, self._group, ical)
		return ical, no_translate
	
	def saveIcal(self, ical: CalendarObject, week_begin: AdeDate) :
		dest_folder = os.path.join(self._group['dest_folder'], self._name)
		if not os.path.exists(dest_folder) :
			os.mkdir(dest_folder)
		dest_file = os.path.join(dest_folder, f"{week_begin} AdeCal.ics")
		with open(dest_file, 'w') as f :
			ical.write(f)
	
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
	
	def getWeek(self) :
		return self._cal['week']
	
	def setUpdate(self) :
		self._cal['update'] = str(AdeDate.today())
	
	def getFullName(self) :
		return self._fullname
