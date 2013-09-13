from . import BuildSystem
import requests

class TravisCI(BuildSystem):
	# States
	FINISHED = ["finished"]
	PENDING = ["created", "started"]

	# Results
	SUCCESS = 0
	FAIL = 1

	def setup(self):
		self.configuration['timeout'] = 10
		self.configuration['project'] = 'jscott1989/mrcontinuousintegrationhead'
		self.load_configuration()

		result = requests.get("https://travis-ci.org/%s" % self.configuration['project']).json()
		self.set_status('tci_last_build_id', result['last_build_id'])
		build_result = requests.get('https://travis-ci.org/builds/%s' % self.status['tci_last_build_id']).json()
		self.set_status('tci_state', build_result['state'])
		if build_result['state'] in self.PENDING:
			self.set_status('state', 'PENDING')
		elif build_result['result'] == self.SUCCESS:
			self.set_status('state', 'SUCCESS')
		else:
			self.set_status('state', 'FAILURE')

	def poll(self):
		result = requests.get("https://travis-ci.org/%s" % self.configuration['project']).json()
		build_id = result['last_build_id']
		build_result = requests.get('https://travis-ci.org/builds/%s' % build_id).json()
		state = build_result['state']

		if self.status['tci_last_build_id'] != build_id or self.status['tci_state'] != state:
			# There has been a change
			self.set_status('tci_last_build_id', build_id)
			self.set_status('tci_state', state)

			result = build_result['result']
			committer_email = build_result['committer_email']
			committer_name = build_result['committer_name']
			message = build_result['message']
			if build_result['state'] in self.PENDING:
				# Currently running
				self.log('Entering pending state')
				self.set_status('state', 'PENDING')
				self.pending(committer_name, message)
			elif build_result['result'] == self.SUCCESS:
				self.log('Entering success state')
				self.set_status('state', 'SUCCESS')
				self.success(committer_name, message)
			else:
				self.log('Entering failure state')
				self.set_status('state', 'FAILURE')
				self.failure(committer_name, message)