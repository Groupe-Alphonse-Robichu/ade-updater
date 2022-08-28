
from icalendar.cal import CalendarConf
from icalendar.utils.date import AdeDate


class GroupConf :

	def __init__(self, group_name, group) :
		self._name = group_name
		self._group = group
		self._start = AdeDate.fromString(group['start'])
		self._end = group['limit']
		if self._end is None :
			self._end = self._start.addDays(180)
		else :
			self._end = AdeDate.fromString(self._end)
	
	def getName(self) -> str :
		return self._name
	
	def getStart(self) -> AdeDate :
		return self._start
	
	def getEnd(self) -> AdeDate :
		return self._end
	
	def getData(self) :
		return self._group
	
	def getDestDir(self) -> str :
		return self._group['dest_folder']
	
	def getAlertChannel(self) :
		return self._group['alert']
	
	def isPastLimit(self) :
		return AdeDate.today() >= self._end

	def getCalendar(self, cal_name) :
		return CalendarConf(cal_name, self)
	
	# func is a callable that takes three arguments :
	#  - The configuration (`CalendarConf` object)
	#  - The notifier
	#  - The dict of states
	# Yields a tuple of three elements :
	#  - A boolean indicating if the configuration must be saved
	#  - A boolean indicating if the states must be saved
	#  - The list of names that couldn't be translated
	#
	# Retruns a tuple of booleans :
	#  - Indicating if the configuration must be saved
	#  - Indicating if the states must be saved
	#
	# Note : if the first boolean yielded by `func` is `False` but there are names 
	# that couldn't be translated, the configuration will be saved anyways
	def forEach(self, func, notifier, states=None) -> "tuple[bool, bool]" :
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
			no_translate = sorted(no_translate)
			save_conf = True
			for elt in no_translate :
				self._group['translate'][elt] = None
			self._group['translate'] = dict(sorted(self._group['translate'].items()))
			notifier.missingTranslation(self, no_translate)

		return save_conf, save_states 