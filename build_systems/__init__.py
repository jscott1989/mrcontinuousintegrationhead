import time

class BuildSystem(object):
	def setup(self):
		pass
	
	def run(self):
		self.setup()
		while True:
			self.poll()
			time.sleep(float(self.configuration['timeout']))