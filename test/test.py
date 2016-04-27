from pyparsing import *
from pydub import *
from pydub.playback import play
import copy
import pyaudio
import wave

song =  AudioSegment.from_wav("test.wav")
song1 = AudioSegment.from_file("myboo.mp3")
clip = song1[26000:37000]
# clip.export("test2.wav", "wav")

# Testing pydub features / Semantics
# pydub does things in milliseconds
five_seconds = 5 * 1000
first_5_seconds = song[:five_seconds]
beginning = first_5_seconds + 1

last_5_seconds = song[-5000:]
end = last_5_seconds - 10

without_middle = beginning + end
without_middle.export("test1.wav", "wav")
test = AudioSegment.from_wav("test1.wav")
# uncomment to play song
# play(test) 

# testing pyparsing features
# determine whether volume + 30 is parsed correctly

beginning.export("control.wav", "wav")
control = AudioSegment.from_wav("control.wav")
# play(control)

# Commands
script = \
"""
    + volume 10
"""

# Testing pyParser / Parser
VOLUME, PITCH = map(Keyword,"volume pitch".split())
# define what commands will look like
rule = Word(printables)("action") \
		+ (VOLUME | PITCH)("effect") \
		+ Word(nums)("value")

rules = OneOrMore(Group(rule))

# TODO: add array to store previous sound files
for r in rules.parseString(script):
	if r.effect == "volume":
		if r.action == "+":
			beginning = first_5_seconds + int(r.value)
		elif r.action == "-":
			beginning = first_5_seconds - int(r.value)
	print r
	print rule

# for action, effect, value in rules.parseString(script):
# 	if effect == "volume":
# 		if action == "+":
# 			beginning = first_5_seconds + int(value)
# 		elif action == "-":
# 			beginning = first_5_seconds - int(value)
beginning = beginning + beginning
beginning.export("volume.wav", "wav")
volume = AudioSegment.from_wav("volume.wav")
# play(volume)

# PITCH TEST
#print beginning.frame_rate 
# beginning.frame_rate *= 2
# print beginning.frame_rate
# play(beginning)
# beginning.export("testfps.wav", "wav")
# play(beginning)

# CHUNK = 1024 
# FORMAT = pyaudio.paInt16 #paInt8
# CHANNELS = 2 
# RATE = 44100 #sample rate
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "output.wav"

# output = AudioSegment.from_wav("output.wav")
# play(output)

# p = pyaudio.PyAudio()

# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK) #buffer

# print("* recording")

# frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data) # 2 bytes(16 bits) per channel

# print("* done recording")

# stream.stop_stream()
# stream.close()
# p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

