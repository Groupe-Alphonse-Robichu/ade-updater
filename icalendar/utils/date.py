from datetime import date, datetime, timezone, timedelta

class AdeDate :

	def __init__(self, d: date) :
		self._date = d
	
	def toDate(self) -> date :
		return self._date
	
	def addDays(self, delta) :
		return AdeDate(applyDelta(self._date, delta))

	def __str__(self) -> str :
		return self._date.strftime('%Y-%m-%d')
	
	def getWeek(self) -> str :
		return self._date.strftime('%Y-%V')
	
	def fromString(s: str) :
		d = datetime.strptime(s, '%Y-%m-%d').date
		return AdeDate(d)
	
	def today(delta=0) :
		return AdeDate(applyDelta(date.today(), delta))
	
	def startAndEndOfWeek(delta=0) -> tuple :
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


def stringToDatetime(t: str) -> datetime :
	return datetime.strptime(t,'%Y%m%dT%H%M%SZ')

def datetimeToString(d: datetime) -> str :
	return d.strftime('%d/%m/%Y %Hh%M')

def utc_to_local(utc_dt: datetime) -> datetime :
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def formatDatetime(d: str) -> str :
	return datetimeToString(utc_to_local(stringToDatetime(d))) 

def formatTimedelta(td: float) -> str :
	td_sec = int(td)
	hours = td_sec // 3600
	minutes = str((td_sec % 3600) // 60).rjust(2, '0')
	return f"{hours}:{minutes}"
