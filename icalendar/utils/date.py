from datetime import date, datetime, timezone, timedelta

class AdeDate :

	def __init__(self, d: date) :
		self._date = d
	
	def toDate(self) -> date :
		return self._date

	def __str__(self) -> str :
		return self._date.strftime('%Y-%m-%d')
	
	def getWeek(self) -> str :
		return self._date.strftime('%Y-%V')
	
	def fromString(s: str) :
		d = datetime.strptime(s, '%Y-%m-%d').date
		return AdeDate(d)
	
	def today(delta=0) :
		d = date.today()
		if delta > 0 :
			d = d + timedelta(days=delta)
		elif delta < 0 :
			d = d - timedelta(days=(-1*delta))
		return AdeDate(d)
	
	def startAndEndOfWeek() -> tuple :
		d = date.today()
		start = d - timedelta(days=d.weekday())
		end = start + timedelta(days=6)
		return (AdeDate(start), AdeDate(end))



def stringToDatetime(t: str) -> datetime :
	return datetime.strptime(t,'%Y%m%dT%H%M%SZ')

def datetimeToString(d: datetime) -> str :
	return d.strftime('%d/%m/%Y %Hh%M')

def utc_to_local(utc_dt: datetime) -> datetime :
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def formatDatetime(d: str) -> str:
	return datetimeToString(utc_to_local(stringToDatetime(d))) 
