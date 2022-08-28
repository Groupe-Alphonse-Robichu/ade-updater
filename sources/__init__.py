
from sources.base import CalendarSource
from sources.custom import SOURCES as __SOURCES

import os
import logging
import pkgutil
from typing import Type

logger = logging.getLogger(__name__)

THIS_DIR   = os.path.dirname(os.path.realpath(__file__))
CUSTOM_DIR = os.path.join(THIS_DIR, 'custom')


def getSources() -> "list[str]" :
	return list(__SOURCES.keys())

def getSource(name: str, global_conf: "dict[str,any]", specific_conf: "dict[str,any]") -> CalendarSource:
	return getSourceClass(name)(global_conf, specific_conf)

def getSourceClass(name: str) -> Type[CalendarSource] :
	if name not in __SOURCES :
		raise ValueError(f"Source {name} doesn't exist")
	return __SOURCES[name]


# Load all modules in the `sources.custom` module in order to populate the list of sources
for loader, module_name, _is_pkg in pkgutil.walk_packages([CUSTOM_DIR], onerror = lambda x: print(x)) :
	# logger.info("Found module %s", module_name)
	loader.find_module(module_name).load_module(module_name)
