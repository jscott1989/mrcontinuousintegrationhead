import bottle
from multiprocessing import Process

class Device(object):
	def __init__(self, *args, **kwargs):
		self.map_gpio()
		self.webserver = Process(target=bottle.run, kwargs=dict(host='0.0.0.0', port=8080))
		self.webserver.daemon = True
		self.webserver.start()
		self.webserver.join()
		super(Device, self).__init__(*args, **kwargs)

	@bottle.route('/')
	@bottle.view('index')
	def index():
		return dict(name="MrContinuousIntegrationHead")