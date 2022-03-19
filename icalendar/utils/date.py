from datetime import date, datetime, timezone, timedelta
from babel.dates import format_datetime

class DateConstants :

	def __init__(self) :
		raise TypeError("The constructor of the DateConstants class should not be called")
	
	TIMEZONE = None

	LOCALE = 'fr_FR'



class AdeDate :

	def __init__(self, d: date) :
		self._dt = d
	
	def toDate(self) -> date :
		return self._dt
	
	def addDays(self, delta) -> "AdeDate" :
		return AdeDate(applyDelta(self._date, delta))
	
	def format(self, fmt='%d/%m/%Y') :
		return self._dt.strftime(fmt)

	def __str__(self) -> str :
		return self._dt.strftime('%Y-%m-%d')
	
	def __ge__(self, d: "AdeDate") -> bool :
		return self._dt >= d._dt

	def __gt__(self, d: "AdeDate") -> bool :
		return self._dt > d._dt

	def __le__(self, d: "AdeDate") -> bool :
		return self._dt <= d._dt

	def __lt__(self, d: "AdeDate") -> bool :
		return self._dt < d._dt
	
	def getWeek(self) -> str :
		return self._dt.strftime('%Y-%V')
	
	def fromString(s: str) -> "AdeDate" :
		d = datetime.strptime(s, '%Y-%m-%d').date()
		return AdeDate(d)
	
	def today(delta=0) -> "AdeDate" :
		return AdeDate(applyDelta(date.today(), delta))
	
	def startAndEndOfWeek(delta=0) -> "tuple[AdeDate, AdeDate]" :
		d = applyDelta(date.today(), delta)
		start = d - timedelta(days=d.weekday())
		end = start + timedelta(days=6)
		return (AdeDate(start), AdeDate(end))


def applyDelta(d: date, delta=0) -> date :
	if delta > 0 :
		return d + timedelta(days=delta)
	elif delta < 0 :
		return d - timedelta(days=(-1*delta))
	return d


def currentWeek(delta=0) -> str :
	return AdeDate.today(delta).getWeek()


class IcalDate :

	def __init__(self, t: "str | datetime", fix_tz=True) :
		self._dt = datetime.strptime(t,'%Y%m%dT%H%M%SZ') if type(t) == str else t
		if fix_tz :
			self._dt = self._dt.replace(tzinfo=timezone.utc).astimezone(tz=DateConstants.TIMEZONE)

	def today(delta=0) -> "IcalDate" :
		return IcalDate(applyDelta(datetime.today(), delta), fix_tz=False)
	
	def toDatetime(self) :
		return self._dt
	
	def getDate(self) -> str:
		return self._dt.strftime('%m/%d/%Y')
	
	def getTimestamp(self) -> int :
		return int(self._dt.timestamp())

	def format(self) :
		return self._dt.strftime('%Y%m%dT%H%M%SZ')
	
	def formatDate(self) :
		return format_datetime(self._dt, 'EEEE dd/MM/YYYY', locale=DateConstants.LOCALE).capitalize()
	
	def formatTime(self) :
		return self._dt.strftime('%H:%M')
	
	def splitDatetime(self) :
		return self.formatDate(), self.formatTime()
	
	def getTimestamp(self) :
		return int(datetime.timestamp(self._dt))

	def __sub__(self, idt) -> timedelta :
		return self._dt - idt._dt
	
	def __str__(self) :
		return self._dt.strftime('%d/%m/%Y %Hh%M')


def formatTimedelta(td: float) -> str :
	td_sec = int(td)
	hours = td_sec // 3600
	minutes = str((td_sec % 3600) // 60).rjust(2, '0')
	return f"{hours}:{minutes}"
