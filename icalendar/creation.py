from icalendar import loadJson, saveJson, CONF_FILE
from icalendar.utils.date import AdeDate

import logging

logger = logging.getLogger(__name__)


def createCalendarGroup(name: str) -> bool :
	data = loadJson(CONF_FILE)
	if '/' in name :
		logger.warning(f"INVALID calendar group name {name}")
	if name in data :
		logger.warning(f"EXISTS calendar group {name}")
		return False
	data[name] = {
		'source': None,
		'project_id': None,
		'resources': [],
		'dest_folder': None,
		'start': str(AdeDate.today()),
		'limit': None,
		'alert': None,
		'ignore': [],
		'translate': {},
		'calendars': {}
	}
	saveJson(data, CONF_FILE)
	logger.info(f"CREATED calendar group {name}")
	return True


def createCalendar(group: str, name: str) -> bool :
	data = loadJson(CONF_FILE)
	if '/' in name :
		logger.warning(f"INVALID calendar name {name}")
	if group not in data :
		logger.warning(f"NOT_FOUND calendar group {group}")
		return False
	if name in data[group] :
		logger.warning(f"EXISTS calendar {name} in calendar group {group}")
		return False
	data[group][name] = {
		'resources': [],
		'notify': None,
		'update': 'never',
		'week': ''
	}
	saveJson(data, CONF_FILE)
	logger.info(f"CREATED calendar {name} in calendar group {group}")
	return True
