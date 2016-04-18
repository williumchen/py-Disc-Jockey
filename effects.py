import copy
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

def pitch(sample, action, value):
	# Has to take integer value
	new_sample = copy.copy(sample)
	if action == "+":
		new_sample.frame_rate *= int(value)
	else:
		new_sample.frame_rate /= int(value)
	return new_sample

def playSample(sample):
	play(sample)

