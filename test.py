from pyparsing import *
from pydub import *
from pydub.playback import play

song =  AudioSegment.from_wav("test.wav")

# testing pydub features
# pydub does things in milliseconds
ten_seconds = 10 * 1000
first_10_seconds = song[:ten_seconds]
beginning = first_10_seconds + 10

last_5_seconds = song[-5000:]
end = last_5_seconds - 10

without_middle = beginning + end
without_middle.export("test1.wav", "wav")

test = AudioSegment.from_wav("test1.wav")
# Uncomment to play song
# play(test) 

# testing pyparsing features
beginning.export("control.wav", "wav")
control = AudioSegment.from_wav("control.wav")
play(control)

script = \
"""
    volume + 30
"""
rule = Word("volume" + "pitch") \
		+ Word(printables) \
		+ Word(nums) 

rules = OneOrMore(Group(rule))

for effect, action, value in rules.parseString(script):
	if effect == "volume":
		if action == "+":
			beginning = first_10_seconds + value
		elif action == "-":
			beginning = first_10_seconds - value
beginning.export("volume.wav", "wav")
volume = AudioSegment.from_wav("volume.wav")
play(volume)
