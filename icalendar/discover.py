from icalendar import loadJson, saveJson, CONF_FILE
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf

import logging
from icalendar.notifiers.base import BaseNotifier

from icalendar.utils.date import AdeDate, stringToDatetime
from icalendar.utils.parser import CalendarObject

logger = logging.getLogger(__name__)


def discoverAccumulator(obj: CalendarObject, events) :
	summary = obj.getProperty('SUMMARY')
	start = stringToDatetime(obj.getProperty('DTSTART'))
	end = stringToDatetime(obj.getProperty('DTEND'))
	td = (end - start).total_seconds()
	if summary not in events :
		events[summary] = [1, td]
	else :
		record = events[summary]
		record[0] += 1
		record[1] += td
	return events


def discoverAll(conf: CalendarConf, notifier: BaseNotifier, _states) :
	ical, no_translate = conf.fetchIcal(conf.getStart(), conf.getEnd())
	notifier.discovered(conf._cal['notify'], conf.getFullName(), ical.accumulate(discoverAccumulator, {}))
	return False, False, no_translate

def discoverRemaining(conf: CalendarConf, notifier: BaseNotifier, _states) :
	ical, no_translate = conf.fetchIcal(str(AdeDate.today()), conf.getEnd())
	notifier.discovered(conf._cal['notify'], conf.getFullName(), ical.accumulate(discoverAccumulator, {}))
	return False, False, no_translate



def discoverAllGroups(func: callable, notifier: BaseNotifier) :
	conf = loadJson(CONF_FILE)
	save_conf = False

	for group_name, group in conf.items() :
		group = GroupConf(group_name, group)
		sc, _ = group.forEach(func, notifier)
		save_conf = save_conf or sc
	
	if sc :
		logger.info("SAVE live configuration")
		saveJson(conf, CONF_FILE)



