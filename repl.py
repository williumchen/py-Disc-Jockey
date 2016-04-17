from cmd import *
from effects import *
from parser import *

class Commands(Cmd):
	intro = "Welcome to the py-disk-jockey shell. Type help or ? to list commands.\n"
	prompt = '(py-DJ)'
	file = None
	curr_song = None

	def do_load(self, arg):
		Commands.curr_song = load_song(arg)
		print "Successfully loaded " + arg

	def default(self, line):
		temp = parse(line)
		if temp.effect == "volume":
			Commands.curr_song = volume(Commands.curr_song, temp.action, temp.value)

	def do_play(self, s):
		# TODO: add keyboard exception
		playSample(Commands.curr_song)

	# Exiting the shell
	def can_exit(self):
		return True
	def do_exit(self, s):
		return True
	def help_exit(self):
		print "Exit the interpreter."
	do_EOF = do_exit
	help_EOF= help_exit	

	# Record and playback
    # def do_record(self, arg):
    #     'Save future commands to filename:  RECORD rose.cmd'
    #     self.file = open(arg, 'w')
    # def do_playback(self, arg):
    #     'Playback commands from a file:  PLAYBACK rose.cmd'
    #     self.close()
    #     with open(arg) as f:
    #         self.cmdqueue.extend(f.read().splitlines())
    # def precmd(self, line):
    #     line = line.lower()
    #     if self.file and 'playback' not in line:
    #         print(line, file=self.file)
    #     return line
    # def close(self):
    #     if self.file:
    #         self.file.close()
    #         self.file = None

if __name__ == '__main__':
	Commands().cmdloop()
