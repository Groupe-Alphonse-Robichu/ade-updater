
from sources.base import CalendarSource

from typing import Type, TypedDict


SOURCES: "TypedDict[str, Type[CalendarSource]]" = {}

def register(clazz: "Type[CalendarSource]", name: str) :
	SOURCES[name] = clazz
