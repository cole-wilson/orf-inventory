import os

def makelabel(text=None, path=None):
	if path != None:
		pass
	elif text != None:
		os.system('echo {} > /dev/usb/lp0'.format(text))
		for feed in range(4):
			os.system('echo > /dev/usb/lp0')
	else:
		os.system('echo "This function was used wrong..." > /dev/usb/lp0')
