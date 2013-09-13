import bottle
from multiprocessing import Process
from datetime import datetime
import pusher

class Device(object):
	test_functions = []
	logs = []

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
		self.register_website_functions()
		self.setup_webserver()
		super(Device, self).__init__(*args, **kwargs)

	def setup_webserver(self):
		bottle.route('/')(bottle.view('index')(self.index))

		bottle.post('/function/<function_id>')(self.function)

		self.webserver = Process(target=bottle.run, kwargs=dict(host='0.0.0.0', port=8080))
		self.webserver.daemon = True
		self.webserver.start()
		self.webserver.join()

	def register_website_functions(self):
		''' Override this '''
		pass

	def register_test_function(self, name, f):
		''' Mark a method as providing a function which can be used to test the functionality of the device '''
		self.test_functions.append([name, f])

	def index(self):
		viewmodel = {
			"log": self.logs
		}

		return dict(viewmodel=viewmodel, name=self.name, test_functions=[[i, f[0]] for i, f in enumerate(self.test_functions)])

	def function(self, function_id):
		self.test_functions[int(function_id)][1]()
		return bottle.redirect('/')