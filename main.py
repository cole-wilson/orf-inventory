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
from RPi import GPIO

# Import custom helper modules
from helpers.handlesql import handlesql, complete
from helpers.handlebarcode import handlebarcode
from helpers.handleadd import handleadd
from helpers.OLED import OLED, last_used, LOGO, logo_set
from helpers.makebarcode import print_label

# Setup readline module:
readline.parse_and_bind('tab: complete')
readline.set_completer(complete)
term = blessed.Terminal()  # For colored output

# Ensure directory exists:
if not os.path.isdir('barcodes'):
	os.mkdir('barcodes')

# Make sure program is running as root
if os.geteuid() != 0:
    print('You must run this script with `sudo` in front as the `pi` user:\n\n\tpi@inventory:~ $ sudo main.py\n\nBye!')
    sys.exit(999)

# Display warning
print(term.red+'WARNING:\n\tOnly exit this script with /quit, not ctrl+c!'+term.normal)
if ('--debug' not in sys.argv and '-d' not in sys.argv):
    for x in range(5):
        print('starting in ' + str(5-x) + ' seconds...                 (to disable wait time run with --debug)', end='\r')
        time.sleep(1)
    print()

# Setup variables
mode = 1
modes = {
    1: 'scan',
    2: 'add (type name)',
    3: 'sql',
    4: 'bash'
}
swpin = 27
dtpin = 18
clkpin = 17
noerror = True
message = ''
source = 'stock'
destination = 'robot'
clickmode = True
prompt = term.green('/? for help') + '  ' + term.cyan+'[{}] > '+term.red
rows, cols = map(int,os.popen('stty size', 'r').read().split())
states = ['stock','robot','testing']
__version__ = "0.1.0"

# "clear" screen
print('\n'*(rows),end='')
# Helper functions: #################################################################
def helptext():
	with term.location(0,round(rows/3)):
		for line in os.popen('figlet Inventory Scanner').read().split('\n'):
			print(term.purple(line).center(cols))
		print((term.red('Welcome to the inventory scanner!')).center(cols))
		print((term.red('Type /? for help. Type /quit to exit.')).center(cols))
		print((term.red('Press the `alt` key (or /mode) to cycle through modes.')).center(cols))
		print((term.red('Type /. to list all records in the items table.')).center(cols))
		print(term.red('Type /barcode to generate extra barcodes.').center(cols))
		print(term.red('ctrl+space, ctrl+left, ctrl+right all act like rotary encoder.').center(cols))
helptext() # Call helptext
def clearhelptext():
	with term.location(0,round(rows/3)-12):
		print(' '.center(cols*10))
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
	cmodestring = 'dest' if clickmode else 'src'
	if mode != 1:
		OLED(mode=cmodestring,source=source,destination=destination,message=['Warning:','Computer not','on scan mode!','switch to scan.'])
	else:
		OLED(mode=cmodestring,source=source,destination=destination,message=[])
def re_sw_click(channel):
	global clickmode
	clickmode = not clickmode
	cmodestring = 'dest' if clickmode else 'src'
	OLED(source=source,destination=destination,mode=cmodestring)
def re_dt_click(channel, force=False):
	global source
	global destination
	clkstate = GPIO.input(clkpin)
	dtstate  = GPIO.input(dtpin)
	if clkstate == 1 and dtstate == 0 or force:
		if clickmode:
			try: destination = states[states.index(destination) + 1]
			except IndexError: destination = states[0]
		else:
			try: source = states[states.index(source) + 1]
			except: source = states[0]
	cmodestring = 'dest' if clickmode else 'src'
	OLED(source=source,destination=destination,mode=cmodestring)
def re_clk_click(channel,force=False):
	global source
	global destination
	clkstate = GPIO.input(clkpin)
	dtstate  = GPIO.input(dtpin)
	if clkstate == 0 and dtstate == 1 or force:
		if clickmode:
			try: destination = states[states.index(destination) - 1]
			except IndexError: destination = states[-1]
		else:
			try: source = states[states.index(source) - 1]
			except: source = states[-1]
	cmodestring = 'dest' if clickmode else 'src'
	OLED(source=source,destination=destination,mode=cmodestring)
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
			elif intext.startswith('/barcode'):
				try:
					amountofcodes = int(input('Number of codes > '))
				except:
					print('Not a valid number!')
				ttprint = input('Text to print > ')
				for x in range(amountofcodes):
					print_label(ttprint)
				continue
			elif intext.startswith('/quit'):
				print(term.normal)
				sys.exit(0)
			elif intext.startswith('/mode'):
				newmode()
				continue
			elif intext.startswith('/.'):
				handlesql('SELECT * FROM items')
				continue
			elif intext.startswith('/?'):
				helptext()
				continue
			print(term.normal+'\033[F'+(message)+(' '*(cols-len(message))) + '\033[F'+(" "*cols)+"\r", end='')
			if mode == 1:
				cmodestring = 'dest' if clickmode else 'src'
				handlebarcode(intext, source, destination, cmodestring)
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
##################################################################
def senseloop():
	global noerror
	global source
	global destination
	global clickmode
	# Setup GPIO:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(clkpin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(dtpin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(swpin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.add_event_detect(clkpin, GPIO.FALLING, callback=re_clk_click, bouncetime=300)
	GPIO.add_event_detect(dtpin, GPIO.FALLING, callback=re_dt_click, bouncetime=300)
	GPIO.add_event_detect(swpin, GPIO.FALLING, callback=re_sw_click, bouncetime=300)
	count = 0
	while noerror: # Checks if screenloop has errored, because that won't stop thread
		time.sleep(0.1)
		if count % 20 == 0 and last_used() + (5*60) < time.time() and not logo_set:
			LOGO()
		if count % 4 == 0:
			with term.location(0,0):
				left = "Inventory Scanner v" + __version__
				right = "Olympia Robotics Federation 4450"
				center = "{} -> {}".format(source,destination)
				print(term.red_on_white(left + center.center(cols-(len(left)+len(right))) + right))
		count += 1
	GPIO.cleanup()
	LOGO()
###################################################################
if __name__ == '__main__':
	try:
		keyboard.add_hotkey('alt', newmode)
		keyboard.add_hotkey('ctrl+tab', newmode)
		keyboard.add_hotkey('ctrl+c', lambda: print('Type /quit to leave'))
		keyboard.add_hotkey('ctrl+l', lambda: print(end=''))
		keyboard.add_hotkey('ctrl+left', lambda: re_clk_click(0,force=True))
		keyboard.add_hotkey('ctrl+right', lambda: re_dt_click(0,force=True))
		keyboard.add_hotkey('ctrl+space', lambda: re_sw_click(0))
		thread1 = Thread(target=screenloop)
		thread2 = Thread(target=senseloop)
		thread1.start()
		thread2.start()
		thread1.join()  # Make the thread blocking
	except:
		sys.exit(314152)
else:
	print('This file must be run as a script, not a module!')
