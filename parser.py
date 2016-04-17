from pyparsing import *

VOLUME, PITCH = map(Keyword,"volume pitch".split())

# define what commands will look like
rule = Word(printables)("action") \
		+ (VOLUME | PITCH)("effect") \
		+ Word(nums)("value")

rules = OneOrMore(Group(rule))

class Command:
	def __init__(self, action, effect, value):
		self.action = action
		self.effect = effect
		self.value = value

def parse(line):
	for r in rules.parseString(line):
		temp = Command(r.action, r.effect, r.value)
	return temp
