from datetime import date, datetime, timezone, timedelta
from babel.dates import format_datetime

DATE_LOCALE = 'fr_FR'


class AdeDate :

	def __init__(self, d: date) :
		self._dt = d
	
	def toDate(self) -> date :
		return self._dt
	
	def addDays(self, delta) :
		return AdeDate(applyDelta(self._date, delta))
	
	def format(self, fmt='%d/%m/%Y') :
		return self._dt.strftime(fmt)

	def __str__(self) -> str :
		return self._dt.strftime('%Y-%m-%d')
	
	def __ge__(self, d) :
		return self._dt >= d._dt
	
	def getWeek(self) -> str :
		return self._dt.strftime('%Y-%V')
	
	def fromString(s: str) :
		d = datetime.strptime(s, '%Y-%m-%d').date()
		return AdeDate(d)
	
	def today(delta=0) :
		return AdeDate(applyDelta(date.today(), delta))
	
	def startAndEndOfWeek(delta=0) -> "tuple[AdeDate, AdeDate]" :
		d = applyDelta(date.today(), delta)
		start = d - timedelta(days=d.weekday())
		end = start + timedelta(days=6)
		return (AdeDate(start), AdeDate(end))


def applyDelta(d, delta=0) -> date :
	if delta > 0 :
		return d + timedelta(days=delta)
	elif delta < 0 :
		return d - timedelta(days=(-1*delta))
	return d


def currentWeek(delta=0) -> str :
	return AdeDate.today(delta).getWeek()


class IcalDate :

	def __init__(self, t: str, clear_tz=True) :
		self._dt = datetime.strptime(t,'%Y%m%dT%H%M%SZ')
		if clear_tz :
			self._dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
	
	def toDatetime(self) :
		return self._dt
	
	def formatDate(self) :
		return format_datetime(self._dt, 'EEEE dd/MM/YYYY', locale=DATE_LOCALE).capitalize()
	
	def formatTime(self) :
		return self._dt.strftime('%H:%M')
	
	def splitDatetime(self) :
		return self.formatDate(), self.formatTime()
	
	def __sub__(self, idt) -> timedelta :
		return self._dt - idt._dt
	
	def __str__(self) :
		return self._dt.strftime('%d/%m/%Y %Hh%M')


def formatTimedelta(td: float) -> str :
	td_sec = int(td)
	hours = td_sec // 3600
	minutes = str((td_sec % 3600) // 60).rjust(2, '0')
	return f"{hours}:{minutes}"
