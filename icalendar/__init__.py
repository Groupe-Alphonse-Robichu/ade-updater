import os
import json
from string import Template

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
CONF_DIR = os.path.join(os.path.dirname(THIS_DIR), 'config')
CONF_FILE = os.path.join(CONF_DIR, 'live.json')
STATES_FILE = os.path.join(CONF_DIR, 'states.json')
ARCHIVE_FILE = os.path.join(CONF_DIR, 'archive.json')
SOURCES_FILE = os.path.join(CONF_DIR, 'sources.json')


def loadJson(path) :
	with open(path, 'r') as f :
		return json.load(f)

def saveJson(data, path) :
	with open(path, 'w') as f :
		json.dump(data, f, indent='\t')


SOURCES = {source: Template(t) for source, t in loadJson(SOURCES_FILE).items()}
