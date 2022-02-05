from icalendar import loadJson, saveJson, CONF_FILE, STATES_FILE, ARCHIVE_FILE
from icalendar.cal import CalendarConf
from icalendar.group import GroupConf
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.date import AdeDate

import os
import logging

logger = logging.getLogger(__name__)


def _computeChanges(old_states: dict, new_states: dict) :
	added = []
	removed = []
	modified = []
	for evt_id, evt_state in old_states.items() :
		if evt_id not in new_states :
			removed.append(evt_state)
			logger.info(f"REMOVED event \"{evt_state[3]}\" ({evt_id})")
		elif evt_state[0] != new_states[evt_id][0] :
			logger.info(f"MODIFIED event \"{evt_state[3]}\" ({evt_id})")
			modified.append(evt_state)
	for evt_id, evt_state in new_states.items() :
		if evt_id not in old_states :
			logger.info(f"ADDED event \"{evt_state[3]}\" ({evt_id})")
			added.append(evt_state)
	return added, removed, modified


def updateCal(conf: CalendarConf, notifier: BaseNotifier, states: dict) :
	start, end = AdeDate.startAndEndOfWeek(2)
	ical, no_translate = conf.fetchIcal(start, end)
	new_states = ical.getStates()
	if conf.weekChanged(2) :
		logger.info(f"UPDATE calendar {conf.getFullName()} : week changed")
		conf.setWeek(2)
		conf.setUpdate()
		states.clear()
		states.update(new_states)
		notifier.weekSchedule(conf, ical)
		conf.saveIcal(ical, start)
		return True, True, no_translate
	else :
		logger.info(f"UPDATE calendar {conf.getFullName()} : check states")
		add, rem, mod = _computeChanges(states, new_states)
		if len(add) + len(rem) + len(mod) > 0 :
			states.clear()
			states.update(new_states)
			conf.setUpdate()
			notifier.changes(conf, add, rem, mod)
			return True, True, no_translate
		return len(no_translate) > 0, False, no_translate


def _archiveGroup(group: GroupConf) :
	logger.info(f"ARCHIVE group {group.getName()}")
	archive = loadJson(ARCHIVE_FILE)
	group_data = group.getData()
	group_data['name'] = group.getName()
	archive.append(group_data)
	saveJson(archive, ARCHIVE_FILE)


def updateAllGroups(notifier: BaseNotifier) :
	conf = loadJson(CONF_FILE)
	states = loadJson(STATES_FILE)
	save_conf = False
	save_states = False

	for group_name, group_data in conf.items() :
		if group_name not in states :
			states[group_name] = {}
		group = GroupConf(group_name, group_data)
		if group.isPastLimit() :
			_archiveGroup(group)
			del conf[group_name]
		else :
			if not os.path.exists(group.getDestDir()) :
				logger.info(f"CREATING directory {group.getDestDir()}")
				os.makedirs(group.getDestDir())
			sc, ss = group.forEach(updateCal, notifier, states[group_name])
			save_conf = save_conf or sc
			save_states = save_states or ss
	
	if save_conf :
		logger.info("SAVE live configuration")
		saveJson(conf, CONF_FILE)
	
	if save_states :
		logger.info("SAVE calendars states")
		saveJson(states, STATES_FILE)



