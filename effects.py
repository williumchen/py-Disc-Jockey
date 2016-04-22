import copy
import threading
from pydub import *
from pydub.playback import play

def load_song(sample):
	"""
	Input: .wav file
	Loads the song to be editted in the REPL interface
	"""
	song = AudioSegment.from_file(sample)
	return song

def volume(sample, action, value):
	"""
	Input: .wav file, +/-, float
	Returns a new sample with the volume adjusted by the specified
	value. 
	"""
	# Decibel to volume ratio: change of 6 dB understood to be twice the volume
	if action == "+":
		new_sample = sample + int(value)*3
	else:
		new_sample = sample - int(value)*3
	return new_sample

# * and / for factor increase, and + and - for linear increase

def pitch(sample, action, value):
	"""
	Input: .wav file, +/-, integer factor
	Returns a new sample with pitch adjusted by the specified value
	Only takes in integers for now, "pseudo-pitch" in that it does
	not preserve the song duration. 
	"""
	# Has to take integer value
	new_sample = copy.copy(sample)
	if action == "+":
		new_sample.frame_rate *= int(value)
	else:
		new_sample.frame_rate /= int(value)
	return new_sample

def concat(file1, file2):
	"""
	Input: 2 .wav files
	Returns a .wav with file2 appended to file1
	"""
	new_sample = file1 + file2
	return new_sample

# Allows for threading so REPL doesn't hang while a song
# is being played

class PlayThread(threading.Thread):
	""" This class allows for multithreading with pyDJ

	More specifically, this class allows for the play function to be 
	run on a separate thread, which allows users to continue editing 
	the song while the song plays.

	"""
	def __init__(self, target, *args):
		self._target = target
		self._args = args
		threading.Thread.__init__(self)

	def run(self):
		self._target(*self._args)

def playSample(sample):
	""" 
	Plays the current song in the REPL interface
	"""
	play(sample)

