
from icalendar.cal import CalendarConf
from icalendar.notifiers.base import BaseNotifier
from icalendar.utils.date import AdeDate


class GroupConf :

	def __init__(self, group_name, group) :
		self._name = group_name
		self._group = group
	
	def getName(self) -> str :
		return self._name
	
	def getData(self) :
		return self._group
	
	def getDestDir(self) -> str :
		return self._group['dest_folder']
	
	def isPastLimit(self) :
		return AdeDate.today() >= AdeDate.fromString(self._group['limit'])

	def getCalendar(self, cal_name) :
		return CalendarConf(cal_name, self._name, self._group)
	
	def forEach(self, func, notifier: BaseNotifier, states=None) -> "tuple[bool, bool]" :
		save_conf = False
		save_states = False
		no_translate = set()
		
		for cal_name in self._group['calendars'] :
			cal = self.getCalendar(cal_name)
			if states is not None :
				if cal_name not in states :
					states[cal_name] = {}
				cal_states = states[cal_name]
			else :
				cal_states = None
			sc, ss, nt = func(cal, notifier, cal_states)
			save_conf = save_conf or sc
			save_states = save_states or ss
			no_translate.update(nt)

		if len(no_translate) > 0 :
			save_conf = True
			for elt in no_translate :
				self._group['translate'][elt] = None
			notifier.missingTranslation(self, no_translate)

		return save_conf, save_states 