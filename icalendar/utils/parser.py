
from collections import deque
from collections.abc import Iterable

import requests
import hashlib
import logging 
from io import StringIO

logger = logging.getLogger(__name__)


class CalendarObject :

	def __init__(self, t):
		self._properties = {}
		self._objects = []
		self._type = t

	def setProperty(self, property: str, value: str) :
		if len(value) > 1 :
			self._properties[property] = value.replace('\\n', '\n').replace('\\,', ',').strip()

	def hasProperty(self, property: str) -> bool :
		return property in self._properties

	def getProperty(self, property: str) -> str :
		return self._properties[property]

	def getPropertyOrDefault(self, property, default="") -> str:
		if property in self._properties :
			return self._properties[property]
		return default

	def removeProperty(self, property: str):
		del self._properties[property]

	def _sortObjects(self) :
		self._objects.sort(key = lambda evt : evt.getProperty('DTSTART'))

	def addObject(self, obj):
		if isinstance(obj, Iterable):
			self._objects.extend(obj)
		else :
			self._objects.append(obj)
		self._sortObjects()
	
	def filterObjects(self, filter: callable) -> int :
		old_len = len(self._objects)
		self._objects = [obj for obj in self._objects if filter(obj)]
		return old_len - len(self._objects)
	
	def mapObjects(self, mapping: callable) -> list :
		return [mapping(obj) for obj in self._objects]
	
	def alterObjects(self, func: callable) :
		for obj in self._objects :
			func(obj)
	
	def accumulate(self, func: callable, accumulator) :
		res = accumulator
		for obj in self._objects :
			res = func(obj, res)
		return res

	def getObjects(self) -> "list[CalendarObject]":
		return self._objects
	
	def getStates(self) :
		return {
			obj.getProperty('UID'): (
				hash(obj), 
				obj.getProperty('DTSTART'), 
				obj.getProperty('DTEND'), 
				obj.getProperty('SUMMARY'), 
				obj.getPropertyOrDefault('LOCATION')
			)
			for obj in self.getObjects()
		}

	def getType(self) :
		return self._type
	
	def write(self, f):
		f.write(f"BEGIN:{self._type}\n")
		for obj in self._objects :
			obj.write(f)
		for k, v in self._properties.items() :
			clean_v = v.replace('\n', '\\n')
			line = f"{k}:{clean_v}"
			while len(line) > 0 :
				if len(line) > 73 :
					f.write(f"{line[:73]}\n")
					line = " " + line[73:]
				else :
					f.write(f"{line}\n")
					line = ""
		f.write(f'END:{self._type}\n')
	
	def getIcs(self) :
		with StringIO() as f :
			self.write(f)
			return f.getvalue()
		
	
	def __hash__(self) :
		prop = self.getProperty('SUMMARY') + ":" + self.getProperty('DTSTART') + "-" + self.getProperty('DTEND') + "@" + self.getPropertyOrDefault('LOCATION')
		prop_hash = hashlib.md5(prop.encode())
		# return prop_hash.hexdigest()
		return int.from_bytes(prop_hash.digest(), 'little')
	
	def fromUrl(url: str) :
		logger.info(f"REQUEST to {url}")
		r = requests.get(url)
		lines: list = r.content.decode('utf8').replace('\r', '').strip().split('\n')
		lines.reverse()
		return readIcs(deque(lines))


def splitLine(line: str) :
	res = line.split(':', 2)
	return (res[0], res[1])

def readIcs(reader: deque) -> CalendarObject :
	line = reader.pop()
	(prop, val) = splitLine(line)
	if prop == 'BEGIN' :
		obj = CalendarObject(val)
		readObj(reader, obj)
		return obj
	raise SyntaxError('Incorrect beginning of .ics file')

def readObj(reader: deque, obj) -> CalendarObject :
	prop = None
	current = None
	while len(reader) > 0 :
		line = reader.pop()
		if line[0] == ' ' :
			current += line[1:]
		else :
			if prop is not None :
				obj.setProperty(prop, current)
			(p, t) = splitLine(line)
			if p == 'BEGIN' :
				prop = None
				evt = CalendarObject(t)
				readObj(reader, evt)
				obj.addObject(evt)
			elif p == 'END' :
				if t != obj.getType() :
					raise SyntaxError(f'Bad end of object : {line}')
				return
			else :
				prop = p
				current = t
