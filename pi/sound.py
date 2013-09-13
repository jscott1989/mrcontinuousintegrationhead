import subprocess

def speak(sentence, pitch=50):
	subprocess.Popen(['espeak "%s" -p %d --stdout | aplay'%(sentence, pitch)], shell=True, close_fds=True)
