from . import Device

from pi import gpio, servo
import threading
import time

COLOUR_RED = "red"
COLOUR_BLUE = "blue"
COLOUR_GREEN = "green"

class ServoShaker(threading.Thread):
	def __init__(self, device):
		self.device = device
		super(ServoShaker, self).__init__()

	def run(self):
		self.stopped = False

		position = self.device.configuration['servo_base_max']
		while not self.stopped:
			if position == self.device.configuration['servo_base_max']:
				position = self.device.configuration['servo_base_min']
			else:
				position = self.device.configuration['servo_base_max']
			self.device.set_servo_position(self.device.configuration['servo_base_id'], position)
			time.sleep(float(self.device.configuration['servo_base_shake_sleep']))

		self.device.set_servo_position(self.device.configuration['servo_base_centre'], position)

	def stop(self):
		self.stopped = True


class MrContinuousIntegrationHead(Device):
	name = "MrContinuousIntegrationHead"
	shaking = None # The thread handling the shaking

	def __init__(self, *args, **kwargs):
		# Default statuses
		self.status['red_eye'] = 'OFF'
		self.status['green_eye'] = 'OFF'
		self.status['blue_eye'] = 'OFF'
		self.status['shaking'] = 'NO'
		self.status['channel_1'] = 0
		self.status['channel_2'] = 0
		self.status['channel_3'] = 0

		self.configuration['red_channel'] = 1
		self.configuration['green_channel'] = 2
		self.configuration['blue_channel'] = 3
		self.configuration['servo_base_id'] = 0
		self.configuration['servo_base_min'] = 60
		self.configuration['servo_base_max'] = 240
		self.configuration['servo_base_centre'] = 150
		self.configuration['servo_base_shake_sleep'] = 0.5
		self.configuration['servo_hat_id'] = 2
		self.configuration['servo_hat_off_level'] = 60
		self.configuration['servo_hat_on_level'] = 240

		super(MrContinuousIntegrationHead, self).__init__(*args, **kwargs)
	
	def map_gpio(self):
		pass
		# gpio.map()

	def register_website_functions(self, *args, **kwargs):
		self.register_test_function('Turn Red Eye On', self.webTurnRedEyeOn)
		self.register_test_function('Turn Red Eye Off', self.webTurnRedEyeOff)
		self.register_test_function('Turn Green Eye On', self.webTurnGreenEyeOn)
		self.register_test_function('Turn Green Eye Off', self.webTurnGreenEyeOff)
		self.register_test_function('Turn Blue Eye On', self.webTurnBlueEyeOn)
		self.register_test_function('Turn Blue Eye Off', self.webTurnBlueEyeOff)
		self.register_test_function('Set Base Position Max', self.webSetBasePositionMax)
		self.register_test_function('Set Base Position Min', self.webSetBasePositionMin)
		self.register_test_function('Set Base Position Centre', self.webSetBasePositionCentre)
		self.register_test_function('Start Shaking', self.webStartShaking)
		self.register_test_function('Stop Shaking', self.webStopShaking)
		self.register_test_function('Push Hat Off', self.webPushHatOff)
		self.register_test_function('Put Hat On', self.webPutHatOn)

	def success(self, committer_name, message):
		# Lower arm

		# Stop shaking
		self.stop_shaking()

		# Blue Eyes
		self.turnEyesOff()
		self.turnEyeOn(COLOUR_BLUE)

		print "Success %s (%s)" % (committer_name, message)

	def failure(self, committer_name, message):
		# Start shaking
		self.start_shaking()

		# Red Eyes
		self.turnEyesOff()
		self.turnEyeOn(COLOUR_RED)
		print "Failure %s (%s)" % (committer_name, message)

	def pending(self, committer_name, message):
		# Raise arm

		# Green Eyes
		self.turnEyesOff()
		self.turnEyeOn(COLOUR_GREEN)
		print "Pending %s (%s)" % (committer_name, message)

	def start_shaking(self):
		if not self.shaking:
			self.log("Starting shaking")
			self.set_status('shaking', 'YES')
			self.shaking = ServoShaker(self)
			self.shaking.start()

	def stop_shaking(self):
		if self.shaking:
			self.log("Stopping shaking")
			self.set_status('shaking', 'NO')
			self.shaking.stop()
			self.shaking = None

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

	def push_hat_off(self):
		self.set_servo_position(self.configuration['servo_hat_id'], self.configuration['servo_hat_off_level'])

	def put_hat_on(self):
		self.set_servo_position(self.configuration['servo_hat_id'], self.configuration['servo_hat_on_level'])


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

	def webSetBasePositionMax(self):
		self.set_servo_position(self.configuration['servo_base_id'], self.configuration['servo_base_max'])

	def webSetBasePositionMin(self):
		self.set_servo_position(self.configuration['servo_base_id'], self.configuration['servo_base_min'])

	def webSetBasePositionCentre(self):
		self.set_servo_position(self.configuration['servo_base_id'], self.configuration['servo_base_centre'])

	def webStartShaking(self):
		self.start_shaking()

	def webStopShaking(self):
		self.stop_shaking()

	def webPushHatOff(self):
		self.push_hat_off()

	def webPutHatOn(self):
		self.put_hat_on()