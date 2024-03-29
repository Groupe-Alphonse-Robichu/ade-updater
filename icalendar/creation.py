from icalendar import loadJson, saveJson, CONF_FILE
from icalendar.utils.date import AdeDate
from sources import getSourceClass

import logging

logger = logging.getLogger(__name__)


def createCalendarGroup(name: str, source_name: str) -> bool :
	source = getSourceClass(source_name)
	data = loadJson(CONF_FILE)
	if '/' in name :
		logger.warning(f"INVALID calendar group name {name}")
	if name in data :
		logger.warning(f"EXISTS calendar group {name}")
		return False
	data[name] = {
		'source': source_name,
		'conf': source.defaultGlobalConf(),
		'dest_folder': None,
		'start': str(AdeDate.today()),
		'limit': None,
		'alert': None,
		'role_id': None,
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
	source = getSourceClass(data[group]['source'])
	if name in data[group]['calendars'] :
		logger.warning(f"EXISTS calendar {name} in calendar group {group}")
		return False
	data[group]['calendars'][name] = {
		'conf': source.defaultSpecificConf(),
		'notify': None,
		'update': 'never',
		'week': ''
	}
	saveJson(data, CONF_FILE)
	logger.info(f"CREATED calendar {name} in calendar group {group}")
	return True
