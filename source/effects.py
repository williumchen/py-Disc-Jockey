import copy
import threading
import pyaudio
import wave
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
	if action == "*":
		new_sample = sample + int(value)*3
	elif action == "+":
		new_sample = sample + int(value)
	elif action == "-":
		new_sample = sample - int(value)
	elif action == "/":
		new_sample = sample - int(value)*3
	else:
		return
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
	if action == "*":
		new_sample.frame_rate *= int(value)
	elif action == "/":
		new_sample.frame_rate /= int(value)
	else:
		return
	return new_sample

def concat(file1, file2):
	"""
	Input: 2 .wav files
	Returns a .wav with file2 appended to file1
	"""
	song1 = AudioSegment.from_file(file1)
	song2 = AudioSegment.from_file(file2)
	new_sample = song1 + song2
	return new_sample

def average(file1, file2):
	"""
	Input: 2 .wav files
	Returns a .wav with both files overlayed
	"""
	song1 = AudioSegment.from_file(file1)
	song2 = AudioSegment.from_file(file2)
	new_sample = song1.overlay(song2)
	return new_sample

def reverse(sample):
	"""
	Input: a .wav file
	Returns a .wav with the audio played backwards
	"""
	new_sample = AudioSegment.reverse(sample)
	return new_sample

# Allows for threading so REPL doesn't hang while a song
# is being played
class Thread(threading.Thread):
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
	try:
		play(sample)
	except:
		print "File not found"

# TODO: Not working, need to figure out threading and keyboard interrupt
def record(end):
	"""
	Input: the name of an export file
	Returns a .wav recording
	Forked from pyAudio tutorials
	"""
	CHUNK = 1024 
	FORMAT = pyaudio.paInt16 #paInt8
	CHANNELS = 2 
	RATE = 44100 # sample rate
	WAVE_OUTPUT_FILENAME = end

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK) #buffer

	frames = []

	while True:
		try:
		    data = stream.read(CHUNK)
		    frames.append(data) # 2 bytes(16 bits) per channel
		except (KeyboardInterrupt, SystemExit):
			break
			stream.stop_stream()
			stream.close()
			p.terminate()
