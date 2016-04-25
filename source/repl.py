from cmd import *
from effects import *
from parser import *

class Commands(Cmd):
	""" This class creates the REPL interface by using the cmd library
	This class essentially ties together the parser and effects
	"""
	intro = "Welcome to the py-disk-jockey shell. Type help or ? to list commands.\n"
	prompt = '(py-DJ) '

	# File name for 'record'
	file = None

	# Current song that is being editted
	# TODO: add multiple songs that can be worked with
	curr_song = None

	# List of edits to the current song
	# TODO: allow users to see the history of edits
	song_history = []

	# List of commands
	command_history = []

	# Each REPL command has a do_(command) and help_(command).
	# The do_(command) actually completes the command whereas the help_(command)
	# provides documentation when user types "help (command)"

	def do_load(self, arg):
		"""
		Loads a song to be editted
		"""
		try: 
			self.curr_song = load_song(arg)
			self.song_history.append(self.curr_song)
			print "Successfully loaded " + arg
		except:
			print "File not found"
	def help_load(self):
		"""
		Help documentation for load
		"""
		print "Loads a song to be editted"

	def do_play(self, s):
		"""
		Plays the currently loaded song with any edits made
		"""
		PlayThread(playSample, self.curr_song).start()

	def help_play(self):
		"""
		Help documentation for play
		"""
		print "Plays the song currently being editted"

	def do_save(self, arg):
		"""
		Saves the edits to a song by exporting to a .wav file named by the user
		"""
		self.curr_song.export(arg, "wav")
	def help_save(self):
		"""
		Help documentation for save
		"""
		print "Exports any changes to the current song to a file name of your choice"

	def do_undo(self, arg):
		"""
		Undoes the most recent edit
		"""
		if len(self.song_history) > 1:
			self.song_history.pop()
			self.command_history.pop()
			self.curr_song = self.song_history[-1]
		else:
			print "There are no more edits to undo"
		# print self.curr_song
	def help_undo(self):
		"""
		Help documentation for undo
		"""
		print "Undoes the most recent change"

	def do_history(self, line):
		"""
		See previous changes to current song
		"""
		print ""
		if not self.command_history:
			print "No history of edits"
		else:
			if line == '':
				for i, command in enumerate(self.command_history):
					print "(" + str(i+1) + ") " + command
			else:
				for i, command in enumerate(self.command_history):
					print "(" + str(i+1) + ") " + command
					if str(i+1) == line:
						break
		print ""
	def help_history(self):
		print "Optionally pass in an integer. Displays previous edits to the current song"

	def do_revert(self, line):
		"""
		Revert song to a certain point in the edit history
		"""
		if not self.command_history:
			print "No existing history of edits"
		else:
			self.curr_song = self.song_history[int(line)]
			del self.song_history[int(line)+1:]
			del self.command_history[int(line):]
	def help_revert(self):
		print "Pass in an integer. Reverts the edited song to that point in the edit history"

	def default(self, line):
		"""
		Handles parsing commands and uses effects.py to create the sound effects
		"""
		if self.curr_song is None:
			print "No loaded song"
		else:
			try:
				temp = parse(line)
				if temp.effect == "volume":
					self.curr_song = volume(self.curr_song, temp.action, temp.value)
				if temp.effect == "pitch":
					self.curr_song = pitch(self.curr_song, temp.action, temp.value)
				self.command_history.append(line)	
				self.song_history.append(self.curr_song)
			except:
				print "Unrecognized command"
	
	# Record and playback commands
	def do_track(self, arg):
		print 'Save future commands to a filename'
		self.file = open(arg, 'w')
	def help_track(self):
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
