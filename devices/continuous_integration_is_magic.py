from . import Device

from pi import gpio

COLOUR_RED = "red"
COLOUR_BLUE = "blue"
COLOUR_GREEN = "green"

RED_CHANNEL = 1
GREEN_CHANNEL = 2
BLUE_CHANNEL = 3

COLOUR_CHANNELS = {COLOUR_RED: RED_CHANNEL, COLOUR_GREEN: GREEN_CHANNEL, COLOUR_BLUE: BLUE_CHANNEL}

class ContinuousIntegrationIsMagic(Device):
	name = "ContinuousIntegrationIsMagic"

	def register_website_functions(self, *args, **kwargs):
		self.register_test_function('Turn Red Eye On', self.webTurnRedEyeOn)
		self.register_test_function('Turn Red Eye Off', self.webTurnRedEyeOff)
		self.register_test_function('Turn Green Eye On', self.webTurnGreenEyeOn)
		self.register_test_function('Turn Green Eye Off', self.webTurnGreenEyeOff)
		self.register_test_function('Turn Blue Eye On', self.webTurnBlueEyeOn)
		self.register_test_function('Turn Blue Eye Off', self.webTurnBlueEyeOff)

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
		self.log("Turning %s light on" % colour)
		gpio.output(COLOUR_CHANNELS[colour], gpio.HIGH)

	def turnEyeOff(self, colour):
		self.log("Turning %s light off" % colour)
		gpio.output(COLOUR_CHANNELS[colour], gpio.LOW)


	def webTurnRedEyeOn(self):
		self.turnEyeOn(COLOUR_RED)

	def webTurnGreenEyeOn(self):
		self.turnEyeOn(COLOUR_GREEN)

	def webTurnBlueEyeOn(self):
		self.turnEyeOn(COLOUR_BLUE)

	def webTurnRedEyeOff(self):
		self.turnEyeOff(COLOUR_RED)

	def webTurnGreenEyeOff(self):
		self.turnEyeOff(COLOUR_GREEN)

	def webTurnBlueEyeOff(self):
		self.turnEyeOff(COLOUR_BLUE)