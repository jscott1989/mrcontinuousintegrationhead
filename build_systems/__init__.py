import time

class BuildSystem(object):
	timeout = 0 # We have this as a variable on the object so that we can change it depending on the state
			# (When the tests are running we want to timeout more often)

	def __init__(self, timeout):
		self.timeout = timeout
	
	def run(self):
		while True:
			self.poll()
			time.sleep(self.timeout)