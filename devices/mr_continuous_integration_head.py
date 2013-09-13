from . import Device

from pi import gpio

class MrContinuousIntegrationHead(Device):
	name = "MrContinuousIntegrationHead"
	
	def map_gpio(self):
		pass
		# gpio.map()

	def success(self, committer_name, message):
		print "Success %s (%s)" % (committer_name, message)

	def failure(self, committer_name, message):
		print "Failure %s (%s)" % (committer_name, message)

	def running(self, committer_name, message):
		print "Running %s (%s)" % (committer_name, message)