from cmd import *
from parser import *

class Commands(Cmd):
	def do_greet(self, line):
		print "hello"

	# Exiting the command line
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

# class HelloWorld(cmd.Cmd):
#     """Simple command processor example."""
    
#     def do_greet(self, line):
#         print "hello"
    
#     def do_EOF(self, line):
#         return True

# if __name__ == '__main__':
#     HelloWorld().cmdloop()	
