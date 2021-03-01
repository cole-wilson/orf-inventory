from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306 as ssd
import subprocess
import time

font = ImageFont.load_default()
#display = ssd.SSD1306_128_64(rst=0)
#display.begin()
#display.clear()
#display.display()
padding = 8

def OLED(source=None,destination=None,message=[],mode='dest',messagecolor=255):
	img = Image.open('logo.png').convert('1')
	draw = ImageDraw.Draw(img)
	if mode == 'src':
		stext = "From: <- {} ->".format(source)
		dtext = "To:      {}".format(destination)
	else:
		stext = "From:    {}".format(source)
		dtext = "To:   <- {} ->".format(destination)
	draw.text((padding,padding), stext, font=font, fill=255)
	draw.text((padding,padding + 10), dtext, font=font, fill=255)
	wrap = 13
	for count, line in enumerate(message):
		draw.text((padding,padding + 20 + (count*9)), line, font=font, fill=messagecolor)
	img.save('output.png')
#	display.clear()
#	display.display()
#	display.image(img)
#	display.display()

if __name__ == '__main__':
	OLED(source='testsrc',destination='testdest',message=["","This is a","test message!"],mode='dest')
