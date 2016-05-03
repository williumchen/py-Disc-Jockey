from pyparsing import *

# Keywords mapped
VOLUME, PITCH, APPEND, REVERSE, RECORD = map(Keyword,"volume pitch append reverse record".split())

# Define the rules to be parsed
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

time_rule = Word(printables)("cut") \
		  + Word(nums)("min") \
		  + Literal(":") \
		  + Word(nums)("sec") \
		  + Word(printables)("to") \
		  + Word(nums)("min2") \
		  + Literal(":") \
		  + Word(nums)("sec2") \

# record_rule = (RECORD)("record") \
# 			+ Word(printables)("end_file")

reverse_rule = (REVERSE)("reverse")
 
rule = basic_rule | concat_rule | average_rule | reverse_rule | time_rule

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

class Reverse:
	"""
	IR for action rule
	"""
	def __init__(self, reverse):
		self.reverse = reverse

class Time:
	"""
	IR for cutting song files
	"""
	def __init__(self, minute, sec, minute2, sec2):
		self.minute = minute
		self.sec = sec
		self.minute2 = minute2
		self.sec2 = sec2

# class Record:
# 	"""
# 	IR for record rule
# 	"""
# 	def __init__(self, record, end):
# 		self.record = record
# 		self.end = end

def parse(line):
	"""
	Parses given user input into IR
	"""
	for r in rules.parseString(line):
		if r.action != '' or r.effect != '' or r.value != '':
			temp = Basic(r.action, r.effect, r.value)
		if r.result != '' or r.file1 != '' or r.file2 != '':
			temp = Combine(r.result, r.file1, r.file2)
		if r.reverse != '':
			temp = Reverse(r.reverse)
		if r.minute != '' or r.sec != '' or r.minute2 != '' or r.sec2 != '':
			temp = Time(r.min, r.sec, r.min2, r.sec2)
		# if r.record != '' or r.end != '':
		# 	temp = Record(r.record, r.end)
	return temp