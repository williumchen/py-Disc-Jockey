from cmd import *
from effects import *
from parser import *

class Commands(Cmd):
	intro = "Welcome to the py-disk-jockey shell. Type help or ? to list commands.\n"
	prompt = '(py-DJ)'
	file = None
	curr_song = None
	song_history = []

	def do_load(self, arg):
		self.curr_song = load_song(arg)
		self.song_history.append(self.curr_song)
		print "Successfully loaded " + arg
	def help_load(self):
		print "Loads a song to be editted"

	def do_play(self, s):
		# TODO: add keyboard exception
		playSample(self.curr_song)
	def help_play(self):
		print "Plays the song currently being editted"

	def do_save(self, arg):
		self.curr_song.export(arg, "wav")
	def help_save(self):
		print "Exports any changes to the current song to a file name of your choice"

	def do_undo(self, arg):
		self.curr_song = self.song_history[-2]
	def help_undo(self):
		print "Undoes the most recent change"

	def default(self, line):
		temp = parse(line)
		if temp.effect == "volume":
			self.curr_song = volume(self.curr_song, temp.action, temp.value)
		self.song_history.append(self.curr_song)
	
	# Record and playback commands
	def do_record(self, arg):
		print 'Save future commands to a filename'
		self.file = open(arg, 'w')

	def do_playback(self,arg):
		print 'Playback commands from a file'
		self.close()
		with open(arg) as f:
			self.cmdqueue.extend(f.read().splitlanes())

	def precmd(self, line):
		line = line.lower()
		if self.file and 'playback' not in line:
			print(line, self.file)
		return line

	def close(self):
		if self.file:
			self.file.close()
			self.file = None

    # Exiting the shell
	def can_exit(self):
		return True
	
	def do_exit(self, s):
		return True
	
	def help_exit(self):
		print "Exit the interpreter."
	do_EOF = do_exit
	help_EOF= help_exit	

if __name__ == '__main__':
	Commands().cmdloop()
