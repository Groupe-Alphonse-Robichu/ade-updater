
from asyncio.log import logger
from icalendar.utils.date import AdeDate
from icalendar.utils.parser import CalendarObject

import logging

logger = logging.getLogger(__name__)


class CalendarSource :

	def getURL(self, begin: AdeDate, end: AdeDate) -> str :
		raise NotImplementedError('Subtypes of CalendarSource must implement the getURL method')

	def fetchIcal(self, begin: AdeDate, end: AdeDate) :
		return CalendarObject.fromUrl(self.getURL(begin, end))
	
	def processEvent(self, obj: CalendarObject, translations: "dict[str,any]", no_translate: "list[str]") -> "CalendarObject | None" :
		summary = obj.getProperty('SUMMARY')
		if summary in translations :
			translation = translations[summary]
			if translation is not None :
				obj.setProperty('SUMMARY', translation)
		else : 
			logger.warning(f"NOT_FOUND translation for {summary}")
			translations[summary] = None
			no_translate.append(summary)
		return obj
	
	def defaultGlobalConf() -> "dict[str,any]" :
		return {}
	
	def defaultSpecificConf() -> "dict[str,any]" :
		return {}
