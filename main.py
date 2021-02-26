#!/usr/bin/python3

# Import modules
from threading import Thread
import time
import keyboard
import os
import sys
import blessed
import readline

# Import modules
from helpers.handlesql import handlesql
from helpers.handlebarcode import handlebarcode
from helpers.handleadd import handleadd

term = blessed.Terminal()  # For colored output

# Display warning
print(term.red+'WARNING:\n\tOnly exit this script with /quit, not ctrl+c!'+term.normal)
if ('--debug' not in sys.argv
            and '-d' not in sys.argv
        ) or os.getenv('DEBUG') == 'true':
    for x in range(5):
        print('starting in ' + str(5-x) + ' seconds...                 (to disable wait time run with --debug)', end='\r')
        time.sleep(1)
    print()

# Make sure program is running as root
if os.geteuid() != 0:
    print('You must run this script with `sudo` in front as the `pi` user:\n\n\tpi@inventory:~ $ sudo main.py\n\nBye!')
    sys.exit(999)

# Setup variables
mode = 1
modes = {
    1: 'SCAN BARCODE',
    2: 'ADD ITEM',
    3: 'SQL SHELL',
    4: 'BASH SHELL'
}
noerror = True
message = ''
source = 'robot'
destination = 'stock'
prompt = term.green('/? for help') + '  ' + term.cyan+'[{}] > '+term.red
rows, cols = map(int,os.popen('stty size', 'r').read().split())

# "clear" screen
print('\n'*(rows-2))

# Helper functions: #################################################################
def movecursor(x,y):
	print('\033[%d;%dH' % (y, x),end="")
	print('Scanned barcode: {}'.format(inp))

def handlebash(inp):
	if inp.startswith('!'):
		os.system(inp[1:])
	else:
		if input(term.red('Are you sure you would like to run {}? [y/n] (to disable message prepend `!` to command) '.format(inp)))[0] == 'y':
			os.system(inp)

def newmode():
	global mode
	print('\r' + (' '*cols), end='')
	mode = 1 if mode==[*modes.keys()][-1] else mode+1
	print('\r'+prompt.format(modes[mode]), end='')

def set_OLED(text):
	print('OLED HAS BEEN SET: {}'.format(text))

# Mainloop functions: ##################################################################

# "screenloop" is run concurrently with
# "senseloop" using a multithreaded
# process. Code displayed on monitor
# should be in screenloop
# Code that runs constantly in the
# background, like sensor checking
# should occur in senseloop.

def screenloop():
	global noerror
	try:
		while True:  # What user sees on screen
			intext = input("\n"+prompt.format(modes[mode])).replace('^[[','')
			if intext == '':
				pass
			elif intext.startswith('/quit'):
				print(term.normal)
				sys.exit(0)
			print(term.normal+'\033[F'+(message)+(' '*(cols-len(message))) + '\033[F'+(" "*cols)+"\r", end='')
			if mode == 1:
				handlebarcode(intext, source, destination)
			elif mode == 2:
				handleadd(intext)
			elif mode == 3:
				handlesql(intext)
			elif mode == 4:
				handlebash(intext)
	except KeyboardInterrupt:
		print('exiting, there may or may not have been an error...')
		noerror = False
def senseloop():
	global noerror # Checks if screenloop has errored, because that won't stop thread
	while noerror:
		time.sleep(0.3)

###################################################################
if __name__ == '__main__':
	try:
		keyboard.add_hotkey('alt', newmode)
		keyboard.add_hotkey('ctrl+c', lambda: print('Type /quit to leave'))
		thread1 = Thread(target=screenloop)
		thread2 = Thread(target=senseloop)
		thread1.start()
		thread2.start()
		thread1.join()  # Make the thread blocking
	except:
		sys.exit(314152)
else:
	print('This file must be run as a script, not a module!')
