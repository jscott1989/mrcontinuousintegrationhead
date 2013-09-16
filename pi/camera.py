import subprocess
import time

def take_picture():
	# Take a picture - put it in picture/picture.jpg
	subprocess.call("raspistill -o picture/picture.jpg", shell=True)
	time.sleep(10)