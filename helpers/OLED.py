from PIL import Image, ImageDraw, ImageFont
import time

font = ImageFont.load_default()

padding = 8

def OLED(source=None,destination=None,message=[],mode='dest',messagecolor='green'):
	a = time.time()
	img = Image.open('logo.png')
	draw = ImageDraw.Draw(img)
	if mode == 'src':
		stext = "From: <- {} ->".format(source)
		dtext = "To:      {}".format(destination)
	else:
		stext = "From:    {}".format(source)
		dtext = "To:   <- {} ->".format(destination)
	draw.text((padding,padding), stext, font=font, fill=(255,255,255))
	draw.text((padding,padding + 10), dtext, font=font, fill=(255,255,255))
	wrap = 13
	for count, line in enumerate(message):
		draw.text((padding,padding + 20 + (count*9)), line, font=font, fill=messagecolor)

	img.save('output.png')
	b = time.time()
if __name__ == '__main__':
	OLED(source='testsrc',destination='testdest',message=["","This is a","test message!"],mode='dest')