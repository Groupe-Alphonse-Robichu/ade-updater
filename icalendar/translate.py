from icalendar.utils.parser import CalendarObject

import logging

logger = logging.getLogger(__name__)


def _cleanLocation(location: str) -> str :
	loc = location.replace('*', ' ')   \
			.replace('(V)', ' ')       \
			.replace('(VPI)', ' ')     \
			.replace(' ,', ',')        \
			.strip()
	return " ".join(loc.split())

def _objTranslate(translate, obj: CalendarObject, no_translate) :
	if obj.hasProperty('LOCATION') :
		obj.setProperty('LOCATION', _cleanLocation(obj.getProperty('LOCATION')))
	summary = obj.getProperty('SUMMARY')
	if summary in translate :
		translation = translate[summary]
		if translation is not None :
			obj.setProperty('SUMMARY', translation)
	else : 
		logger.warning(f"NOT_FOUND translation for {summary}")
		translate[summary] = None
		no_translate.append(summary)

def filterAndTranslate(name, group, ical: CalendarObject) -> "list[str]" :
	ignore = group['ignore']
	translate = group['translate']
	nb_ignored = ical.filterObjects(lambda obj: obj.getProperty('SUMMARY') not in ignore)
	if nb_ignored > 0 :
		logger.info(f"IGNORE {nb_ignored} elements from calendar {name}")
	no_translate = []
	ical.alterObjects(lambda obj: _objTranslate(translate, obj, no_translate))
	return no_translate
