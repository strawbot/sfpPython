# messages  Rob Chapman  Jan 30, 2011

from __future__ import print_function
import queue, time
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

maxMessages = 1000 # maximum queue size before blocking input

textout = None

def setTextOutput(f): # output can be redirected to a different place
	global textout
	textout = f

def defaultWrite(string, style=''): # default output is to std out
	print(string)

setTextOutput(defaultWrite)

def messageQueue(): # output to message queue for isolation
	messageq = queue.Queue(maxMessages)
	def writeq(string, style=''):
		messageq.put((string, style))
	setTextOutput(writeq)
	return messageq

# messages
def note(string):
	textout('\n'+string, style='note')

def warning(string): # mark a message for formatting
	textout('\n'+string, style='warning')

def error(string):
	textout('\n'+string, style='error')

def message(string, style=''): # mark a message for formatting
	textout(string, style)

def write(text): # route the message to file or window
	message(text)
	
def messageDump(who,s=[], text=0): # dump message in hex or text to terminal
	# s could be a string, character or integer
	framedump = ''
	if s:
		# note(type(s))
		if type(s) == type(0):
			s = [s]
		elif type(s[0]) == type('a'):
			if type(s) == type([]):
				s = list(map(ord, s[0]))
			else:
				s = list(map(ord, s))
		if text:
			framedump = ''.join([chr(i) if i >= ord(' ') and i <= ord('~')  else ' ' for i in s])
		else:
			framedump = ' '.join([hex(i)[2:].upper().zfill(2) for i in s])
	note(who + framedump)

class stdMessage(object): # for redirecting standard out
	@classmethod
	def write(cls, string):
		textout(string)
