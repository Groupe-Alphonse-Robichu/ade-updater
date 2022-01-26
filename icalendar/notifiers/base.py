
class BaseNotifier :

	def missingTranslation(self, channel, summaries) :
		raise NotImplementedError

	def discovered(self, channel, event_counts) :
		raise NotImplementedError
	
	def weekSchedule(self, channel, events) :
		raise NotImplementedError
	
	def changes(self, channel, insertions, deletions, modifications) :
		raise NotImplementedError
