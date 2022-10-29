
from sources.base import CalendarSource
from sources.custom import register
from icalendar.utils.date import AdeDate
from icalendar.utils.parser import CalendarObject

import re
import string
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

course_code_reg = re.compile(r'Course code: ([A-Z0-9]+)')

URL_TEMPLATE = string.Template('https://cloud.timeedit.net/ltu/web/schedule1/ri.ics?sid=${sid}&p=${begin}-${end}&objects=${objects}&e=${e}&enol=t')
DATE_FORMAT  = '%Y%m%d'
E_DATE_FORMAT  = '%y%m%d'

SID_FIELD = 'sid'
OBJECTS_FIELD = 'objects'


class LUTSource(CalendarSource) :

	def __init__(self, global_conf: "dict[str,any]", specific_conf: "dict[str,any]") :
		for field in [SID_FIELD, OBJECTS_FIELD] :
			if field not in specific_conf :
				raise KeyError(f"field {field} not found in configuration for LUTSource")
		self.sid = specific_conf[SID_FIELD]
		self.objects = specific_conf[OBJECTS_FIELD]

	def fetchIcal(self, begin: AdeDate, end: AdeDate) :
		res = super().fetchIcal(begin, end)
		res.filterObjects(lambda obj: _dateFilter(obj, begin, end))
		return res

	def getURL(self, begin: AdeDate, end: AdeDate) -> str:
		return URL_TEMPLATE.substitute(
			sid = self.sid,
			objects = self.objects,
			e = datetime.now().strftime(E_DATE_FORMAT),
			begin = begin.format(DATE_FORMAT),
			end = end.format(DATE_FORMAT)
		)

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
		return { SID_FIELD: None, OBJECTS_FIELD: None }


register(LUTSource, 'ltu')


def _dateFilter(obj: CalendarObject, start: AdeDate, end: AdeDate) -> bool :
	evt_start = obj.getStartDate().toAdeDate()
	return evt_start >= start and evt_start <= end
