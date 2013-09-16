import subprocess

def set_position(n, position):
	subprocess.call("sudo echo %s=%d > /dev/servoblaster" % (n, position), shell=True)