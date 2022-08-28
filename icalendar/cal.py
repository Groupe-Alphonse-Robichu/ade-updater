from icalendar.translate import filterAndTranslate
from icalendar.utils.parser import CalendarObject
from icalendar.utils.date import AdeDate, currentWeek
from sources.base import CalendarSource
import sources

import os
import logging

logger = logging.getLogger(__name__)


class CalendarConf :

	def __init__(self, cal_name, group) :
		group_name = group.getName()
		group_data = group.getData()
		self._name = cal_name
		self._fullname = f"{group_data['source']}_{group_name}_{cal_name}"
		self._group_name = group_name
		self._group = group
		self._cal = group_data['calendars'][cal_name]
		self._source = sources.getSource(group_data['source'], group_data['conf'], self._cal['conf'])

	def getSource(self) -> CalendarSource :
		return self._source

	def getStart(self) -> AdeDate :
		return self._group.getStart()
	
	def getEnd(self) -> AdeDate :
		return self._group.getEnd()

	def getGroup(self) :
		return self._group

	def fetchIcal(self, start: AdeDate, end: AdeDate) -> "tuple[CalendarObject, list[str]]" :
		ical = CalendarObject.fromUrl(self._source.getURL(start, end))
		no_translate = filterAndTranslate(self, ical)
		return ical, no_translate
	
	def saveIcal(self, ical: CalendarObject, name: "AdeDate | str | None") :
		dest_folder = os.path.join(self._group.getDestDir(), self._name)
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
	
	def getNotify(self) -> str :
		return self._cal['notify']
	
	def getRoleId(self) :
		return self._group.getData()['role_id']
	
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
