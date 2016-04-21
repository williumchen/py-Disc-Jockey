from cmd import *
from effects import *
from parser import *

# Class for the REPL interface that uses the cmd library
class Commands(Cmd):
	intro = "Welcome to the py-disk-jockey shell. Type help or ? to list commands.\n"
	prompt = '(py-DJ)'

	# File name for 'record'
	file = None

	# Current song that is being editted
	# TODO: add multiple songs that can be worked with
	curr_song = None

	# List of edits to the current song
	# TODO: allow users to see the history of edits
	song_history = []

	# Each REPL command has a do_(command) and help_(command).
	# The do_(command) actually completes the command whereas the help_(command)
	# provides documentation when user types "help (command)"

	# Loads a song to be editted
	def do_load(self, arg):
		self.curr_song = load_song(arg)
		self.song_history.append(self.curr_song)
		print "Successfully loaded " + arg
	def help_load(self):
		print "Loads a song to be editted"

	# Plays a song with any edits made
	# TODO: Multi-threading to allow users to edit while playing the song
	def do_play(self, s):
		print "Now playing . . ."
		PlayThread(playSample, self.curr_song).start()

	def help_play(self):
		print "Plays the song currently being editted"

	# Saves the edits to a song by exporting to a .wav file named by the user
	def do_save(self, arg):
		self.curr_song.export(arg, "wav")
	def help_save(self):
		print "Exports any changes to the current song to a file name of your choice"

	# Undoes the most recent edit
	def do_undo(self, arg):
		if len(self.song_history) > 0:
			self.song_history.pop()
			self.curr_song = self.song_history[-1]
		else:
			print "There are no more edits to undo"
		# print self.curr_song
	def help_undo(self):
		print "Undoes the most recent change"

	# Handles parsing commands and uses effects.py to create the sound effects
	def default(self, line):
		try:
			temp = parse(line)
			if temp.effect == "volume":
				self.curr_song = volume(self.curr_song, temp.action, temp.value)
			if temp.effect == "pitch":
				self.curr_song = pitch(self.curr_song, temp.action, temp.value)
			self.song_history.append(self.curr_song)
		except:
			print "Unrecognized command"
	
	# Record and playback commands
	def do_record(self, arg):
		print 'Save future commands to a filename'
		self.file = open(arg, 'w')
	def help_record(self):
		print "Records the edits of a particular song"

	def do_playback(self,arg):
		print 'Playback commands from a file'
		self.close()
		with open(arg) as f:
			self.cmdqueue.extend(f.read().splitlanes())
	def help_playback(self):
		print "Loads edits of a previous session"

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
