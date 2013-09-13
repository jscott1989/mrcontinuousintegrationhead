try:
	from RPi import GPIO

	from GPIO import IN, OUT, BOARD, BCM, HIGH, LOW, output

	def map(mode, channels):
		GPIO.setmode(mode)
		for channel, value in channels.items():
			GPIO.setup(channel, value)
except ImportError:
	# No RPi - probably not running on a PI - simulate this
	IN = "in"
	OUT = "out"
	BOARD = "board"
	BCM = "bcm"
	HIGH = 1
	LOW = 0

	_mode = None
	_channels = [{"mode": None, "value": LOW} for x in range(10)]

	def map(mode, channels):
		_mode = mode
		for channel, value in channels.items():
			_channels[channel]["mode"] = value

	def output(channel, value):
		_channels[channel]["value"] = value