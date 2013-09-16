import subprocess

def set_position(n, position):
	subprocess.call("sudo echo %d=%d > /dev/servoblaster" % (n, position), shell=True)