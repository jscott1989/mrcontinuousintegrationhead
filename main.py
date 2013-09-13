'''
	MrContinuousIntegrationHead
'''
TIMEOUT = 10

from devices.mr_continuous_integration_head import MrContinuousIntegrationHead
from devices.continuous_integration_is_magic import ContinuousIntegrationIsMagic
from build_systems.travisci import TravisCI

if __name__ == "__main__":
	class MrTravisCIHead(TravisCI, MrContinuousIntegrationHead):
		pass

	MrTravisCIHead(timeout=TIMEOUT, project="jscott1989/mrcontinuousintegrationhead").run()