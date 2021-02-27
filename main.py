#!/usr/bin/python3

# Import modules
from threading import Thread
import time
import keyboard
import os
import sys
import blessed
import readline
import random

# Import modules
from helpers.handlesql import handlesql
from helpers.handlebarcode import handlebarcode
from helpers.handleadd import handleadd
from helpers.OLED import OLED

term = blessed.Terminal()  # For colored output

# Ensure directory exists:
if not os.path.isdir('barcodes'):
	os.mkdir('barcodes')

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
    1: 'scan',
    2: 'add (type name)',
    3: 'sql',
    4: 'bash'
}
noerror = True
message = ''
source = 'robot'
destination = 'stock'
prompt = term.green('/? for help') + '  ' + term.cyan+'[{}] > '+term.red
rows, cols = map(int,os.popen('stty size', 'r').read().split())

__version__ = "0.1.0"

# "clear" screen
print('\n'*(rows-2))
# Helper functions: #################################################################
def helptext():
	with term.location(0,round(rows/2)):
		print((term.red('Welcome to the inventory scanner!')).center(cols))
		print((term.red('Type /? for help. Type /quit to exit.')).center(cols))
		print((term.red('Press the `alt` key (or /mode) to cycle through modes.')).center(cols))
		print((term.red('Type /. to list all records in the items table.')).center(cols))
helptext()
def clearhelptext():
	with term.location(0,round(rows/2)-3):
		print(' '.center(cols*5))
def movecursor(x,y):
	print('\033[%d;%dH' % (y, x),end="")
	print('Scanned barcode: {}'.format(inp))

def handlebash(inp):
	if inp.startswith(','):
		os.system(inp[1:])
	else:
		if (input(term.red('Are you sure you would like to run {}? [y/n] (to disable message prepend `,` to command) '.format(inp)))+"y")[0] == 'y':
			os.system(inp)

def newmode():
	global mode
	print('\r' + (' '*cols), end='')
	mode = 1 if mode==[*modes.keys()][-1] else mode+1
	print('\r'+prompt.format(modes[mode]), end='')

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
		cleared = False
		while True:  # What user sees on screen
			intext = input("\n"+prompt.format(modes[mode])).replace('^[[','')
			if intext == '':
				pass
			elif intext.startswith('/quit'):
				print(term.normal)
				sys.exit(0)
			elif intext == '/mode':
				newmode()
				continue
			elif intext == '/.':
				handlesql('SELECT * FROM items')
				continue
			elif intext.startswith('/?'):
				helptext()
				continue
			print(term.normal+'\033[F'+(message)+(' '*(cols-len(message))) + '\033[F'+(" "*cols)+"\r", end='')
			if mode == 1:
				handlebarcode(intext, source, destination)
			elif mode == 2:
				handleadd(intext)
			elif mode == 3:
				handlesql(intext)
			elif mode == 4:
				handlebash(intext)
			if not cleared:
				cleared = True
				clearhelptext()
	except BaseException as err:
		if str(err) != "0":
			print('exiting, there may or may not have been an error...\n\t{}'.format(err))

		else:
			print('Bye!')
		noerror = False
def senseloop():
	global noerror
	global source
	global destination
	count = 0
	while noerror: # Checks if screenloop has errored, because that won't stop thread
		OLED(source=source, destination=destination)
		time.sleep(0.5)
		if count % 4 == 0:
			source = random.choice(['robot','stock','testing'])
			destination = random.choice(['robot','stock','testing'])
			OLED(source=source,destination=destination,message=[str(time.time())])
			with term.location(0,0):
				left = "Inventory Scanner v" + __version__
				right = "Olympia Robotics Federation 4450"
				center = "{} -> {}".format(source,destination)
				print(term.red_on_white(left + center.center(cols-(len(left)+len(right))) + right))
		count += 1

###################################################################
if __name__ == '__main__':
	try:
		keyboard.add_hotkey('alt', newmode)
		keyboard.add_hotkey('ctrl+tab', newmode)
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
