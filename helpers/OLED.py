from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306 as ssd
import subprocess
import time

cmode = '1'
font = ImageFont.load_default()
display = ssd.SSD1306_128_64(rst=0)
display.begin()
img = Image.open('logo.png').convert(cmode)
display.image(img)
display.display()
padding = 8
fill = 255


def OLED(source=None,destination=None,message=[],mode='dest',messagecolor=255):
	img = Image.open('logo.png').convert(cmode)
	draw = ImageDraw.Draw(img)
	if mode == 'src':
		stext = "From: <- {} ->".format(source)
		dtext = "To:      {}".format(destination)
	else:
		stext = "From:    {}".format(source)
		dtext = "To:   <- {} ->".format(destination)
	draw.text((padding,padding), stext, font=font, fill=fill)
	draw.text((padding,padding + 10), dtext, font=font, fill=fill)
	draw.line((padding,padding + 20, 128 - padding, padding + 20), fill=fill)
	wrap = 13
	for count, line in enumerate(message):
		draw.text((padding,padding + 20 + (count*9)), line, font=font, fill=messagecolor)
	img.save('output.png')
	display.display()
	display.image(img)
	display.display()

OLED(source='stock',destination='robot',message=["","Welcome to the","inventory", "scanner!"],mode='dest')
