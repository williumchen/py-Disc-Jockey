from pyparsing import *

VOLUME, PITCH = map(Keyword,"volume pitch".split())

# define what commands will look like
rule = Word(printables)("action") \
		+ (VOLUME | PITCH)("effect") \
		+ Word(nums)("value")

rules = OneOrMore(Group(rule))

def getEffect(line):
	for r in rules.parseString(line):
		return r.effect

def getValue(line):
	for r in rules.parseString(line):
		return r.value

def getAction(line):
	for r in rules.parseString(line):
		return r.action
