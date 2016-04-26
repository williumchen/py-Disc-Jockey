from pyparsing import *

# Keywords mapped
VOLUME, PITCH, APPEND = map(Keyword,"volume pitch append".split())

# Define the rules to be parsed
# TODO: Time stamp rules?
basic_rule = Word(printables)("action") \
		+ (VOLUME | PITCH)("effect") \
		+ Word(nums)("value")

concat_rule = Word(printables)("result") \
			+ Literal("=") \
			+ Word(printables)("file1") \
			+ (APPEND)("append") \
			+ Word(printables)("file2")

average_rule = Word(printables)("result") \
			 + Literal("=") \
			 + Word(printables)("file1") \
			 + Literal("+") \
			 + Word(printables)("file2")
 
rule = basic_rule | concat_rule | average_rule

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

class Combine:
	"""
	IR for concat rule
	"""
	def __init__(self, result, file1, file2):
		self.result = result
		self.file1 = file1
		self.file2 = file2

def parse(line):
	"""
	Parses given user input into IR
	"""
	for r in rules.parseString(line):
		if r.action != '' or r.effect != '' or r.value != '':
			temp = Basic(r.action, r.effect, r.value)
		if r.result != '' or r.file1 != '' or r.file2 != '':
			temp = Combine(r.result, r.file1, r.file2)
	return temp