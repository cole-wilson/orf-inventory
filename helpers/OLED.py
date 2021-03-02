from PIL import Image, ImageDraw, ImageFont
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306 as ssd
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, sh1106
import subprocess
import time

cmode = '1'
font = ImageFont.load_default()
#display = ssd.SSD1306_128_64(rst=0)
display = sh1106(i2c(port=1, address=0x3C))
#display.begin()
img = Image.open('logo.png').convert(cmode)
display.display(img)
#display.display()
padding = 2
fill = 255
lastused = 0
logo_set = False

def last_used():
	return lastused
def LOGO():
	global logo_set
	logo_set = True
	bg = Image.new('1',(128,64),'black')
	img = Image.open('cropped-logo.png').convert(cmode).resize((64,64))
	bg.paste(img,(32,0))
	#display.display()
	display.display(bg)
	#display.display()

def OLED(source=None,destination=None,message=[],mode='dest',messagecolor=255):
	global lastused
	global logo_set
	logo_set = False
	img = Image.open('logo.png').convert(cmode)
	draw = ImageDraw.Draw(img)
	if mode == 'src':
		stext = "From: {}".format(source)
		dtext = "To:   {}".format(destination)
	else:
		stext = "From: {}".format(source)
		dtext = "To:   {}".format(destination)
	draw.text((padding,padding), stext, font=font, fill=fill)
	draw.text((padding,padding + 10), dtext, font=font, fill=fill)
	draw.line((padding,padding + 20, 128 - padding, padding + 20), fill=fill)
	wrap = 13
	for count, line in enumerate(message):
		draw.text((padding,padding + 20 + (count*9)), line, font=font, fill=messagecolor)
	img.save('output.png')
	#display.display()
	display.display(img)
	#display.display()
	lastused = time.time()

OLED(source='stock',destination='robot',message=["","Welcome to the","inventory", "scanner!"],mode='dest')
