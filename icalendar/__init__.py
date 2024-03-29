import os
import json

import logging

logger = logging.getLogger(__name__)

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
CONF_DIR = os.path.join(os.path.dirname(THIS_DIR), 'config')
CONF_FILE = os.path.join(CONF_DIR, 'live.json')
STATES_FILE = os.path.join(CONF_DIR, 'states.json')
ARCHIVE_FILE = os.path.join(CONF_DIR, 'archive.json')


def loadJson(path) :
	with open(path, 'r') as f :
		return json.load(f)

def saveJson(data, path) :
	with open(path, 'w') as f :
		json.dump(data, f, indent='\t')

if not os.path.exists(CONF_DIR) :
	os.mkdir(CONF_DIR)

for file, default in [(CONF_FILE, {}), (STATES_FILE, {}), (ARCHIVE_FILE, [])] :
	if not os.path.exists(file) :
		logger.info(f"CREATE file {file}")
		saveJson(default, file)
