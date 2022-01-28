
from icalendar.cal import CalendarConf


class GroupConf :

	def __init__(self, group_name, group) :
		self._name = group_name
		self._group = group
	
	def getName(self) -> str :
		return self._name
	
	def getData(self) :
		return self._data

	def getCalendar(self, cal_name) :
		return CalendarConf(cal_name, self._name, self._group)
	
	def forEach(self, func, states=None) -> "tuple[bool, bool]" :
		save_conf = False
		save_states = False
		
		for cal_name in self._group['calendars'] :
			cal = self.getCalendar(cal_name)
			if states is not None :
				if cal_name not in states :
					states[cal_name] = []
				cal_states = states[cal_name]
			else :
				cal_states = None
			sc, ss = func(cal, cal_states)
			save_conf = save_conf or sc
			save_states = save_states or ss

		return save_conf, save_states 