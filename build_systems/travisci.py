from . import BuildSystem
import requests

class TravisCI(BuildSystem):
	# States
	FINISHED = ["finished"]
	PENDING = ["created", "started"]

	# Results
	SUCCESS = 0
	FAIL = 1

	last_build_id = 0
	last_state = ''

	def __init__(self, timeout, project):
		self.project = project
		result = requests.get("https://travis-ci.org/%s" % self.project).json()
		self.last_build_id = result['last_build_id']
		build_result = requests.get('https://travis-ci.org/builds/%s' % self.last_build_id).json()
		self.last_state = build_result['state']

		super(TravisCI, self).__init__(timeout)

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
			if build_result['state'] in self.PENDING:
				# Currently running
				self.running(committer_name, message)
			elif build_result['result'] == self.SUCCESS:
				self.success(committer_name, message)
			else:
				self.failure(committer_name, message)