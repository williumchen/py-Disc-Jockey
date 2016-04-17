from pydub import *
from pydub.playback import play

def load_song(sample):
	song = AudioSegment.from_wav(sample)
	return song

def volume(sample, action, value):
	if action == "+":
		sample = sample + int(value)
	else:
		sample = sample - int(value)
	return sample

def playSample(sample):
	play(sample)

