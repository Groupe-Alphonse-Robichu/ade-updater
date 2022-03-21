from icalendar import loadJson, saveJson, CONF_FILE
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.date import AdeDate, IcalDate
from icalendar.utils.parser import CalendarObject

import logging

logger = logging.getLogger(__name__)


def discoverAccumulator(obj: CalendarObject, events) :
	summary = obj.getProperty('SUMMARY')
	start = IcalDate(obj.getProperty('DTSTART'))
	end = IcalDate(obj.getProperty('DTEND'))
	td = (end - start).total_seconds()
	if summary not in events :
		events[summary] = [1, td]
	else :
		record = events[summary]
		record[0] += 1
		record[1] += td
	return events


def discoverAll(conf: CalendarConf, notifier: BaseNotifier, _states) -> "tuple[bool, bool, dict]":
	nt, ical = discoverBetweenDates(conf, notifier, conf.getStart(), conf.getEnd())
	conf.saveIcal(ical, None)
	return False, False, nt


def discoverRemaining(conf: CalendarConf, notifier: BaseNotifier, _states) -> "tuple[bool, bool, dict]" :
	nt, ical = discoverBetweenDates(conf, notifier, str(AdeDate.today()), conf.getEnd())
	conf.saveIcal(ical, "remaining")
	return False, False, nt

def discoverBetweenDates(conf: CalendarConf, notifier: BaseNotifier, begin, end) :
	ical, no_translate = conf.fetchIcal(begin, end)
	notifier.discovered(conf, ical.accumulate(discoverAccumulator, {}), begin, end)
	return no_translate, ical



# `func` is a callable that takes three arguments :
#  - The configuration (`CalendarConf` object)
#  - The notifier
#  - The dict of states (in this case it will be `None`)
# Yields a tuple of three elements :
#  - A boolean indicating if the configuration must be saved (most likely `False`)
#  - A boolean indicating if the states must be saved (always `False` in this case)
#  - The list of names that couldn't be translated
#
# Note : if the first boolean yielded by `func` is `False` but there are names 
# that couldn't be translated, the configuration will be saved anyways
def discoverAllGroups(func: callable, notifier: BaseNotifier) :
	conf = loadJson(CONF_FILE)
	save_conf = False

	for group_name, group in conf.items() :
		group = GroupConf(group_name, group)
		sc, _ = group.forEach(func, notifier)
		save_conf = save_conf or sc
	
	if save_conf :
		logger.info("SAVE live configuration")
		saveJson(conf, CONF_FILE)



