
from icalendar.utils.parser import CalendarObject
from sources.custom import register
from sources.base import CalendarSource
from icalendar.utils.date import AdeDate

import string
from typing import Union, Iterable

URL_TEMPLATE = string.Template('http://ade.insa-rennes.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=${resources}&projectId=${project}&calType=ical&firstDate=${start}&lastDate=${end}')
DATE_FORMAT  = '%Y-%m-%d'

RESOURCES_FIELD = 'resources'
PROJECT_FIELD   = 'project_id'


class INSARennesSource(CalendarSource) :

	def __init__(self, global_conf: "dict[str,any]", specific_conf: "dict[str,any]") :
		if RESOURCES_FIELD not in global_conf and RESOURCES_FIELD not in specific_conf :
			raise KeyError('field %s not found in configuration for INSARennesSource', RESOURCES_FIELD)
		self.resources = None
		if RESOURCES_FIELD in global_conf :
			self.resources = _formatResources(global_conf[RESOURCES_FIELD])
		if RESOURCES_FIELD in specific_conf :
			self.resources = ((self.resources + ",") if self.resources is not None else "") \
							 + _formatResources(specific_conf[RESOURCES_FIELD])
		if PROJECT_FIELD not in global_conf :
			raise KeyError('field %s not found in global configuration for INSARennesSource', PROJECT_FIELD)
		self.project_id = global_conf[PROJECT_FIELD]

	def getURL(self, begin: AdeDate, end: AdeDate) -> str:
		return URL_TEMPLATE.substitute(
			project   = self.project_id,
			resources = self.resources,
			start     = begin.format(DATE_FORMAT),
			end       = end.format(DATE_FORMAT)
		)

	def processEvent(self, obj: CalendarObject, translations: "dict[str,any]", no_translate: "list[str]") -> "CalendarObject | None" :
		if obj.hasProperty('LOCATION') :
			obj.setProperty('LOCATION', _cleanLocation(obj.getProperty('LOCATION')))
		return super().processEvent(obj, translations, no_translate)
	
	def defaultGlobalConf() -> "dict[str,any]" :
		return {
			PROJECT_FIELD: None,
			RESOURCES_FIELD: []
		}
	
	def defaultSpecificConf() -> "dict[str,any]" :
		return { RESOURCES_FIELD: [] }


register(INSARennesSource, 'insa_rennes')


def _formatResources(resources: "Union[str,Iterable]") :
	return resources if type(resources) == str else ','.join(str(x) for x in resources)

def _cleanLocation(location: str) -> str :
	loc = [
		" ".join(l.replace('*', ' ').replace('(V)', ' ').replace('(VPI)', ' ').strip().split())
		for l in location.split(',')
	]
	return ", ".join(loc)
