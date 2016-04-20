import copy
import threading
from pydub import *
from pydub.playback import play

def load_song(sample):
	song = AudioSegment.from_file(sample)
	return song

def volume(sample, action, value):
	# Decibel to volume ratio: change of 6 dB understood to be twice the volume
	if action == "+":
		new_sample = sample + int(value)*3
	else:
		new_sample = sample - int(value)*3
	return new_sample

# * and / for factor increase, and + and - for linear increase

def pitch(sample, action, value):
	# Has to take integer value
	new_sample = copy.copy(sample)
	if action == "+":
		new_sample.frame_rate *= int(value)
	else:
		new_sample.frame_rate /= int(value)
	return new_sample

def concat(file1, file2):
	new_sample = file1 + file2
	return new_sample

# Allows for threading so REPL doesn't hang while a song
# is being played

class PlayThread(threading.Thread):
	def __init__(self, target, *args):
		self._target = target
		self._args = args
		threading.Thread.__init__(self)

	def run(self):
		self._target(*self._args)

def playSample(sample):
	play(sample)

