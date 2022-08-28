from icalendar.translate import filterAndTranslate
from icalendar.utils.parser import CalendarObject
from icalendar.utils.date import AdeDate, currentWeek
import sources

import os
import logging

logger = logging.getLogger(__name__)


class CalendarConf :

	def __init__(self, cal_name, group_name, group) :
		self._name = cal_name
		self._fullname = f"{group['source']}_{group_name}_{cal_name}"
		self._group_name = group_name
		self._group = group
		self._cal = group['calendars'][cal_name]
		if not sources.hasSource(group['source']) :
			raise ValueError("Source %s doesn't exist", group['source'])
		self._source = sources.getSource(group['source'], self._group['conf'], self._cal['conf'])
		self._start = AdeDate.fromString(self._group['start'])
		self._end = self._group['limit']
		if self._end is None :
			self._end = self._start.addDays(180)

	
	def fetchIcal(self, start: AdeDate, end: AdeDate) -> "tuple[CalendarObject, list[str]]" :
		ical = CalendarObject.fromUrl(self._source.getURL(start, end))
		no_translate = filterAndTranslate(self._fullname, self._group, ical)
		return ical, no_translate
	
	def saveIcal(self, ical: CalendarObject, name: "AdeDate | str | None") :
		dest_folder = os.path.join(self._group['dest_folder'], self._name)
		if not os.path.exists(dest_folder) :
			logger.info(f"CREATING directory {dest_folder}")
			os.mkdir(dest_folder)
		if name is None :
			dest_file = os.path.join(dest_folder, 'AdeCal.ics')
		else :
			dest_file = os.path.join(dest_folder, f"{name} AdeCal.ics")
		logger.info(f"SAVING file {dest_file}")
		with open(dest_file, 'w') as f :
			ical.write(f)
	
	def getStart(self) -> AdeDate:
		return self._start
	
	def getEnd(self) -> str :
		return self._end
	
	def getNotify(self) -> str :
		return self._cal['notify']
	
	def getRoleId(self) :
		return self._group['role_id']
	
	def weekChanged(self, delta=0) -> bool :
		week = currentWeek(delta)
		return self._cal['week'] != week

	def setWeek(self, delta=0) :
		self._cal['week'] = currentWeek(delta)
	
	def getWeek(self) :
		return self._cal['week']
	
	def setUpdate(self) :
		self._cal['update'] = str(AdeDate.today())
	
	def getUpdate(self) :
		return self._cal['update']
	
	def getFullName(self) :
		return self._fullname
