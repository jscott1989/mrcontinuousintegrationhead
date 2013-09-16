import bottle
import thread
from datetime import datetime
import pusher
import os
import sys
import yaml
from collections import OrderedDict
import random

from pi import gpio, servo, sound, camera

class Device(object):
	test_functions = []
	logs = []
	status = OrderedDict()
	configuration = OrderedDict()

	def load_configuration(self):
		try:
			self.configuration = OrderedDict(self.configuration.items() + yaml.load(open('config.yml').read()).items())
		except IOError:
			pass # Config file not set yet - will use defaults

	def set_status(self, key, value):
		self.status[key] = value
		self.pusher[self.name].trigger('change-status', {'key': key, 'value': value})

	def log(self, message):
		time = datetime.now().strftime('%d-%m-%y %H:%M')
		logstring = '%s : %s ' % (time, message)
		self.logs.append(logstring)
		with open("log.txt", "a") as logfile:
			logfile.write('%s\n' % logstring)
		self.pusher[self.name].trigger('log', {'logstring': logstring})

	def __init__(self, *args, **kwargs):
		try:
			self.logs = open('log.txt').read().split('\n')[:-1] # Cut off the last empty line
		except IOError:
			pass # Log file doesn't exist yet

		self.pusher = pusher.Pusher(
		  app_id='54097',
		  key='2c0e2063352f3e58148f',
		  secret='e0ffde2228c53caa1408'
		)
		self.map_gpio()

		self.register_test_function('Success', self.webSuccess)
		self.register_test_function('Pending', self.webPending)
		self.register_test_function('Failure', self.webFailure)

		self.register_website_functions()
		thread.start_new_thread(self.setup_webserver, ())
		super(Device, self).__init__(*args, **kwargs)

	def setup_webserver(self):
		bottle.route('/')(bottle.view('index')(self.index))

		bottle.post('/clear_log')(self.clear_log)
		bottle.post('/config')(self.config)
		bottle.post('/function/<function_id>')(self.function)
		bottle.run(host='0.0.0.0', port=8080)

	def register_website_functions(self):
		''' Override this '''
		pass

	def register_test_function(self, name, f):
		''' Mark a method as providing a function which can be used to test the functionality of the device '''
		self.test_functions.append([name, f])

	def index(self):
		viewmodel = {
			"log": self.logs,
			"status": [{"key": k, "value": v} for k, v in self.status.items()],
		}

		return dict(configuration=self.configuration, viewmodel=viewmodel, name=self.name, test_functions=[[i, f[0]] for i, f in enumerate(self.test_functions)])

	def clear_log(self):
		self.logs = []
		open('log.txt', 'w').close()
		self.pusher[self.name].trigger('clear-log')

	def function(self, function_id):
		self.test_functions[int(function_id)][1]()
		return bottle.redirect('/')

	def config(self):
		self.configuration = OrderedDict(self.configuration.items() + bottle.request.forms.items())
		with open('config.yml', 'w') as outfile:
			outfile.write(yaml.dump(self.configuration, default_flow_style=True))

	def gpio_output(self, channel, value):
		self.set_status('channel_%s' % channel, value)
		self.log("Setting channel %s to %s" % (channel, value))
		gpio.output(int(channel), int(value))

	def set_servo_position(self, servo_id, position):
		self.log("Setting servo position to %s" % position)
		self.set_status('servo_%s_position' % servo_id, position)
		servo.set_position(0, position)

	def speak(self, message, pitch):
		self.log("Saying '%s' at pitch %d" % (message, pitch))
		sound.speak(message, pitch)

	def play(self, f):
		self.log("Playing '%s'" % f)
		sound.play(f)

	def take_picture(self):
		self.log("Taking picture")
		camera.take_picture()

	def webSuccess(self):
		self.success("Test Committer", "Test Message")

	def webPending(self):
		self.pending("Test Committer", "Test Message")

	def webFailure(self):
		self.failure("Test Committer", "Test Message")