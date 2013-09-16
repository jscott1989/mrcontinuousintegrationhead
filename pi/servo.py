import subprocess

def set_position(n, position):
	subprocess.call("sudo echo %s=%s > /dev/servoblaster" % (n, position), shell=True)