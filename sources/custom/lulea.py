
from sources.base import CalendarSource
from sources.custom import register
from icalendar.utils.date import AdeDate, IcalDate
from icalendar.utils.parser import CalendarObject

import re
import logging

logger = logging.getLogger(__name__)

course_code_reg = re.compile(r'Course code: ([A-Z0-9]+)')

URL_FIELD = 'url'


class LUTSource(CalendarSource) :

	def __init__(self, global_conf: "dict[str,any]", specific_conf: "dict[str,any]") :
		if URL_FIELD not in specific_conf :
			raise KeyError('field %s not found in configuration for LUTSource', URL_FIELD)
		self.url = specific_conf[URL_FIELD]

	def fetchIcal(self, begin: AdeDate, end: AdeDate) :
		res = super().fetchIcal(begin, end)
		res.filterObjects(lambda obj: _dateFilter(obj, begin, end))
		return res

	def getURL(self, _begin: AdeDate, _end: AdeDate) -> str:
		return self.url

	def processEvent(self, obj: CalendarObject, translations: "dict[str,any]", no_translate: "list[str]") -> "CalendarObject | None" :
		if obj.hasProperty('LOCATION') :
			location = obj.getProperty('LOCATION')
			if location.startswith('Room: ') :
				obj.setProperty('LOCATION', location[6:])
		course_type = obj.getProperty('SUMMARY').split(', ')[0]
		course_code_search = course_code_reg.findall(obj.getProperty('SUMMARY'))
		if len(course_code_search) > 0 :
			course_code = course_code_search[0]
			summary = course_code
			if course_code in translations :
				translation = translations[course_code]
				if translation is not None :
					summary = translation
			else : 
				logger.warning(f"NOT_FOUND course for code {course_code}")
				translations[course_code] = None
				no_translate.append(course_code)
			summary = f"{summary} ({course_type.lower()})"
		else :
			summary = course_type
		obj.setProperty('SUMMARY', summary)
		return obj
	
	def defaultSpecificConf() -> "dict[str,any]" :
		return { URL_FIELD: None }


register(LUTSource, 'ltu')


def _dateFilter(obj: CalendarObject, start: AdeDate, end: AdeDate) -> bool :
	evt_start = obj.getStartDate().toAdeDate()
	return evt_start >= start and evt_start <= end
