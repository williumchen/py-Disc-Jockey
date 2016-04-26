from pyparsing import *

# Keywords mapped
VOLUME, PITCH = map(Keyword,"volume pitch".split())

# Define the rules to be parsed
# TODO: Time stamp rules?
basic_rule = Word(printables)("action") \
		+ (VOLUME | PITCH)("effect") \
		+ Word(nums)("value")

concat_rule = Word(printables)("file1") \
			+ Literal("+") \
			+ Word(printables)("file2")

rule = basic_rule | concat_rule

rules = OneOrMore(Group(rule))

# IR
class Basic:
	"""
	IR for the basic rule
	"""
	def __init__(self, action, effect, value):
		self.action = action
		self.effect = effect
		self.value = value

class Concat:
	"""
	IR for concat rule
	"""
	def __init__(self, file1, file2):
		self.file1 = file1
		self.file2 = file2

def parse(line):
	"""
	Parses given user input into IR
	"""
	for r in rules.parseString(line):
		if r.action != '' or r.effect != '' or r.value != '':
			temp = Basic(r.action, r.effect, r.value)
		if r.file1 != '' or r.file2 != '':
			temp = Concat(r.file1, r.file2)
	return temp