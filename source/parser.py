from pyparsing import *

VOLUME, PITCH = map(Keyword,"volume pitch".split())

# define what commands will look like

basic_rule = Word(printables)("action") \
		+ (VOLUME | PITCH)("effect") \
		+ Word(nums)("value")

# rule = concat_rule | action_rule
rule = basic_rule
# concat_rule = Word(printables)("file1") \
# 			+ Literal("+") \
# 			+ Word(printables)("file2")

# concat_rule.parseString("asdf + asdf")
# check object returned
# setParseAction

rules = OneOrMore(Group(rule))

class Basic:
	def __init__(self, action, effect, value):
		self.action = action
		self.effect = effect
		self.value = value

# class Concat:
# 	def __init__(self, file1, file2):
# 		self.file1 = file1
# 		self.file2 = file2

def parse(line):
	for r in rules.parseString(line):
		temp = Basic(r.action, r.effect, r.value)
	return temp

# TODO: try catch exception
# def parse_concat(line):
# 	for r in rules.parseString(line):
# 		temp = Concat(r.file1, r.file2)
# 	return temp
