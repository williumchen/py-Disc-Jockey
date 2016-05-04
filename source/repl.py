from cmd import *
from effects import *
from parser import *

class Commands(Cmd):
	""" This class creates the REPL interface by using the cmd library
	This class essentially ties together the parser and effects
	"""
	intro = "Welcome to the py-disk-jockey command-line interface. Type help or ? to list commands.\n"
	prompt = '(py-DJ) '

	# File name for 'record'
	file = None

	# Current song that is being editted
	curr_song = None
	song_name = None
	# List of songs loaded
	song_list = {}

	# List of edits to the current song
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
			self.song_name = arg
			self.curr_song = load_song(arg)
			# self.song_history.append(self.curr_song)
			if self.song_list.get(arg) is None:
				self.song_list[arg] = [self.curr_song, [], [self.curr_song]]
			else:
				self.song_list[arg] = [self.curr_song, self.song_list[arg][1], self.song_list[arg][2]]
			# print self.song_list
			print "Successfully loaded " + arg
		except:
			print "File not found"
	def help_load(self):
		"""
		Help documentation for load
		"""
		print "Loads a song to be editted"

	def do_edit(self, arg):
		"""
		Sets a song as current song
		"""
		if arg == '' and self.song_name != None:
			print "Currently editting: " + self.song_name
		elif self.song_name == None:
			print "Not currently editting any song. Refer to 'help load' for more information"
		else:
			try:
				self.song_name = arg
				self.curr_song = self.song_list[arg][0]
				print "Currently editting: " + arg
			except:
				print "Song not found in workspace. Try loading the song. Refer to 'help load' for more information"
	def help_edit(self):
		print "Selects a loaded song to be editted"

	def do_files(self, arg):
		"""
		Displays songs loaded
		"""
		print ""
		for i, key in enumerate(self.song_list):
			print "(" + str(i+1) + ") " + str(key),
			if key == self.song_name:
				print " *",
			print ""
		print ""
	def help_files(self):
		print "Displays all loaded songs"

	def do_play(self, s):
		"""
		Plays the currently loaded song with any edits made
		"""
		Thread(playSample, self.curr_song).start()
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
		try:
			if arg == '':
				self.song_list[self.song_name][1].pop()
				self.song_list[self.song_name][2].pop()
				self.song_list[self.song_name][0] = self.song_list[self.song_name][2][-1]
				self.curr_song = self.song_list[self.song_name][0]
				# self.curr_song = self.song_history[-1]
			elif arg != '':
				for x in range(int(arg)):
					self.song_list[self.song_name][1].pop()
					self.song_list[self.song_name][2].pop()
					self.song_list[self.song_name][0] = self.song_list[self.song_name][2][-1]
		except:
			print "There are no more edits to undo"
	def help_undo(self):
		"""
		Help documentation for undo
		"""
		print "Undoes the most recent change"

	def do_history(self, line):
		"""
		See previous changes to current song
		"""
		# TODO: history defaults to 5, typing history all will show everything
		if not self.song_list[self.song_name][1]:
		# if not self.command_history:
			print "No history of edits"
		else:
			print ""
			if line == '':
				# for i, command in enumerate(reversed(self.command_history)):
				for i, command in enumerate(reversed(self.song_list[self.song_name][1])):
					print "(" + str(i+1) + ") " + command
			else:
				# for i, command in enumerate(reversed(self.command_history)):
				for i, command in enumerate(reversed(self.song_list[self.song_name][1])):
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
		# if not self.command_history:
		try: 
			if not self.song_list[self.song_name][1]:
				print "No existing history of edits"
			else:
				self.song_list[self.song_name][0] = list(reversed(self.song_list[self.song_name][2]))[int(line)-1]
				self.curr_song = self.song_list[self.song_name][0]
				# Song history
				del self.song_list[self.song_name][2][-(int(line)-1):]
				# Command history
				del self.song_list[self.song_name][1][-(int(line)-1):]
		except:
			print "Cannot reach specified state"
	def help_revert(self):
		print "Pass in an integer. Reverts the edited song to that point in the edit history"

	def default(self, line):
		"""
		Handles parsing commands and uses effects.py to create the sound effects
		"""
		try:
			temp = parse(line)
		# TODO: Look into threading with record + keyboard interrupt
		# 	if isinstance(temp, Record):
		# 		Thread(record, temp.end).start()
		# 		self.do_load(temp.end)
		# 	else:
		# 		print "No loaded song"
			if self.curr_song is None:
				print "No loaded song"
			if isinstance(temp, Basic):
				if temp.effect == "volume":
					self.curr_song = volume(self.curr_song, temp.action, temp.value)
				elif temp.effect == "pitch":
					self.curr_song = pitch(self.curr_song, temp.action, temp.value)
			elif isinstance(temp, Combine):
				if "append" in line:
					self.curr_song = concat(temp.file1, temp.file2)
					self.do_save(temp.result)
					self.do_load(temp.result)
				elif "+" in line:
					self.curr_song = average(temp.file1, temp.file2)
					self.do_save(temp.result)
					self.do_load(temp.result)
			elif isinstance(temp, Reverse):
				self.curr_song = reverse(self.curr_song)
			elif isinstance(temp, Time):
				self.curr_song = cut(self.curr_song, temp.minute, temp.sec, temp.minute2, temp.sec2)
			if self.curr_song != None:
				self.song_list[self.song_name][1].append(line)
				self.song_list[self.song_name][2].append(self.curr_song)
			else:
				self.curr_song = self.song_list[self.song_name][2][-1]
				print "Unrecognized command"
		except:
			print "Unrecognized command"
	
	# Misc help commands
	def help_volume(self):
		print "+,-,*,/ volume (integer value)"
	def help_pitch(self):
		print "+,- pitch (integer value)"
	def help_concat(self):
		print "Adds two sound files end to end"
		print "result = file1.wav append file2.wav"
	def help_average(self):
		print "Overlays two sound files"
		print "result = file1.wav + file2.wav"
	def help_reverse(self):
		print "Reverses a sound file"
		print "reverse"
	def help_cut(self):
		print "Cut out a segment of a sound file at specified time intervals"
		print "cut 0:03 to 0:08"

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
