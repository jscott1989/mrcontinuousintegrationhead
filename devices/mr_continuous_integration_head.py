from . import Device

from pi import gpio, servo
import threading
import time

COLOUR_RED = "red"
COLOUR_BLUE = "blue"
COLOUR_GREEN = "green"

RED_CHANNEL = 1
GREEN_CHANNEL = 2
BLUE_CHANNEL = 3

COLOUR_CHANNELS = {COLOUR_RED: RED_CHANNEL, COLOUR_GREEN: GREEN_CHANNEL, COLOUR_BLUE: BLUE_CHANNEL}

SERVO_BASE_ID = 0

class ServoShaker(threading.Thread):
	def __init__(self, device):
		self.device = device
		super(ServoShaker, self).__init__()

	def run(self):
		self.stopped = False

		position = 240
		while not self.stopped:
			if position == 240:
				position = 60
			else:
				position = 240
			self.device.set_servo_position(SERVO_BASE_ID, position)
			time.sleep(0.5)

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
		self.status['servo_0_position'] = 0
		self.status['channel_1'] = 0
		self.status['channel_2'] = 0
		self.status['channel_3'] = 0

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
		self.register_test_function('Start Shaking', self.webStartShaking)
		self.register_test_function('Stop Shaking', self.webStopShaking)

	def success(self, committer_name, message):
		print "Success %s (%s)" % (committer_name, message)

	def failure(self, committer_name, message):
		print "Failure %s (%s)" % (committer_name, message)

	def running(self, committer_name, message):
		print "Running %s (%s)" % (committer_name, message)

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

	def set_servo_position(self, servo_id, position):
		self.log("Setting servo position to %d" % position)
		self.set_status('servo_%d_position' % servo_id, position)
		servo.set_position(0, position)

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
		self.gpio_output(COLOUR_CHANNELS[colour], gpio.HIGH)

	def turnEyeOff(self, colour):
		self.log("Turning %s light off" % colour)
		self.set_status('%s_eye' % colour, 'OFF')
		self.gpio_output(COLOUR_CHANNELS[colour], gpio.LOW)


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
		self.set_servo_position(SERVO_BASE_ID, 240)

	def webSetBasePositionMin(self):
		self.set_servo_position(SERVO_BASE_ID, 60)

	def webStartShaking(self):
		self.start_shaking()

	def webStopShaking(self):
		self.stop_shaking()