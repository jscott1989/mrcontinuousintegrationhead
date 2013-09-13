from . import Device

COLOUR_RED = "red"
COLOUR_BLUE = "blue"
COLOUR_GREEN = "green"

RED_CHANNEL = 1
GREEN_CHANNEL = 2
BLUE_CHANNEL = 3

COLOUR_CHANNELS = {COLOUR_RED: RED_CHANNEL, COLOUR_GREEN: GREEN_CHANNEL, COLOUR_BLUE: BLUE_CHANNEL}

class ContinuousIntegrationIsMagic(Device):
	def map_gpio(self):
		pass
		# gpio.map(gpio.BOARD, {COLOUR_CHANNELS[COLOUR_RED]: gpio.OUT, COLOUR_CHANNELS[COLOUR_GREEN]: gpio.OUT, COLOUR_CHANNELS[COLOUR_BLUE]: gpio.OUT})

	def success(self, committer_name, message):
		print "Success %s (%s)" % (committer_name, message)

	def failure(self, committer_name, message):
		print "Failure %s (%s)" % (committer_name, message)

	def running(self, committer_name, message):
		print "Running %s (%s)" % (committer_name, message)

	def turnEyesOn(self):
		self.turnEyeOn(COLOUR_RED)
		self.turnEyeOn(COLOUR_GREEN)
		self.turnEyeOn(COLOUR_BLUE)

	def turnEyesOff(self):
		self.turnEyeOff(COLOUR_RED)
		self.turnEyeOff(COLOUR_GREEN)
		self.turnEyeOff(COLOUR_BLUE)

	def turnEyeOn(self, colour):
		gpio.output(COLOUR_CHANNELS[colour], gpio.HIGH)

	def turnEyeOff(self, colour):
		gpio.output(COLOUR_CHANNELS[colour], gpio.LOW)