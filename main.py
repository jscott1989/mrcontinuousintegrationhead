'''
	MrContinuousIntegrationHead
'''


import requests
import time

# States
FINISHED = ["finished"]
PENDING = ["created", "started"]

SUCCESS = 0
FAIL = 1

TIMEOUT = 10

class MrContinuousIntegrationHead(object):
	timeout = 0 # We have this as a variable on the object so that we can change it depending on the state
				# (When the tests are running we want to timeout more often)
	def main(self):
		self.timeout = TIMEOUT

		while True:
			self.poll()
			time.sleep(self.timeout)

	def success(self, committer_name, message):
		print "Success %s (%s)" % (committer_name, message)

	def failure(self, committer_name, message):
		print "Failure %s (%s)" % (committer_name, message)

	def running(self, committer_name, message):
		print "Running %s (%s)" % (committer_name, message)

class MrTravisCIHead(MrContinuousIntegrationHead):
	last_build_id = 0
	last_state = ''

	def __init__(self, project):
		self.project = project
		result = requests.get("https://travis-ci.org/%s" % self.project).json()
		self.last_build_id = result['last_build_id']
		build_result = requests.get('https://travis-ci.org/builds/%s' % self.last_build_id).json()
		self.last_state = build_result['state']

	def poll(self):
		result = requests.get("https://travis-ci.org/%s" % self.project).json()
		build_id = result['last_build_id']
		build_result = requests.get('https://travis-ci.org/builds/%s' % build_id).json()
		state = build_result['state']

		if self.last_build_id != build_id or self.last_state != state:
			# There has been a change
			last_build_id = build_id

			result = build_result['result']
			committer_email = build_result['committer_email']
			committer_name = build_result['committer_name']
			message = build_result['message']
			print build_result
			if build_result['state'] in PENDING:
				# Currently running
				self.running(committer_name, message)
			elif build_result['result'] == SUCCESS:
				self.success(committer_name, message)
			else:
				self.failure(committer_name, message)

if __name__ == "__main__":
	MrTravisCIHead("jscott1989/mrcontinuousintegrationhead").main()