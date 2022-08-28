from icalendar.utils.parser import CalendarObject

import logging

logger = logging.getLogger(__name__)


def filterAndTranslate(cal, ical: CalendarObject) -> "list[str]" :
	ignore = cal.getGroup().getData()['ignore']
	translate = cal.getGroup().getData()['translate']
	nb_ignored = ical.filterObjects(lambda obj: obj.getProperty('SUMMARY') not in ignore)
	if nb_ignored > 0 :
		logger.info(f"IGNORE {nb_ignored} elements from calendar {cal.getFullName()}")
	no_translate = []
	ical.replaceObjects(lambda obj: cal.getSource().processEvent(obj, translate, no_translate))
	return no_translate
