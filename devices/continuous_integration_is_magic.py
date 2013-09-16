from . import Device

from pi import gpio
import bottle
import flickrapi
import random
import time

COLOUR_RED = "red"
COLOUR_BLUE = "blue"
COLOUR_GREEN = "green"

class ContinuousIntegrationIsMagic(Device):
	name = "ContinuousIntegrationIsMagic"

	def __init__(self, *args, **kwargs):
		# Default statuses
		self.status['red_eye'] = 'OFF'
		self.status['green_eye'] = 'OFF'
		self.status['blue_eye'] = 'OFF'
		self.status['channel_1'] = 0
		self.status['channel_2'] = 0
		self.status['channel_3'] = 0
		self.status['latest_picture'] = '<img id="pony_picture" style="width:500px" src="/picture.jpg">'

		self.configuration['flickr_key'] = '83ee24ab46fcbcb14e9f31971f149175'
		self.configuration['flickr_secret'] = '2fadce29881de31f'

		self.configuration['red_channel'] = 11
		self.configuration['green_channel'] = 15
		self.configuration['blue_channel'] = 13

		bottle.route('/picture.jpg')(self.host_picture)

		super(ContinuousIntegrationIsMagic, self).__init__(*args, **kwargs)

	def register_website_functions(self, *args, **kwargs):
		self.register_test_function('Turn Red Eye On', self.webTurnRedEyeOn)
		self.register_test_function('Turn Red Eye Off', self.webTurnRedEyeOff)
		self.register_test_function('Turn Green Eye On', self.webTurnGreenEyeOn)
		self.register_test_function('Turn Green Eye Off', self.webTurnGreenEyeOff)
		self.register_test_function('Turn Blue Eye On', self.webTurnBlueEyeOn)
		self.register_test_function('Turn Blue Eye Off', self.webTurnBlueEyeOff)
		self.register_test_function('Take Picture', self.webTakePicture)

	def host_picture(self):
		return bottle.static_file('picture.jpg', root='picture')

	def take_picture(self):
		super(ContinuousIntegrationIsMagic, self).take_picture()
		self.set_status('latest_picture', '<img id="pony_picture" style="width:500px" src="/picture.jpg?pid=%d">' % random.randint(0, 9999999))
		flickr = flickrapi.FlickrAPI(self.configuration['flickr_key'], self.configuration['flickr_secret'])
		(token, frob) = flickr.get_token_part_one(perms='write')
		if not token: raw_input("Press ENTER after you authorized this program")
		flickr.get_token_part_two((token, frob))
		flickr.upload('picture/picture.jpg')


	def map_gpio(self):
		pass
		gpio.map(gpio.BOARD, {self.configuration['red_channel']: gpio.OUT, self.configuration['green_channel']: gpio.OUT, self.configuration['blue_channel']: gpio.OUT})

	def success(self, committer_name, message):
		# Blue eye
		self.turnEyeOn(COLOUR_BLUE);
		print "Success %s (%s)" % (committer_name, message)

	def failure(self, committer_name, message):
		# Red eye
		self.turnEyeOn(COLOUR_RED);
		print "Failure %s (%s)" % (committer_name, message)

		time.sleep(3)
		self.take_picture()

	def pending(self, committer_name, message):
		# Green eye
		self.turnEyeOn(COLOUR_GREEN);
		print "Pending %s (%s)" % (committer_name, message)

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
		self.set_status('%s_eye' % colour, 'ON')
		self.gpio_output(self.configuration[colour + '_channel'], gpio.HIGH)

	def turnEyeOff(self, colour):
		self.log("Turning %s light off" % colour)
		self.set_status('%s_eye' % colour, 'OFF')
		self.gpio_output(self.configuration[colour + '_channel'], gpio.LOW)


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

	def webTakePicture(self):
		self.take_picture()