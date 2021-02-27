from PIL import Image, ImageDraw, ImageFont
import time

font = ImageFont.load_default()

padding = 10

def OLED(source=None,destination=None):
	a = time.time()
	img = Image.new('1', (128,64))
	draw = ImageDraw.Draw(img)
	draw.text((padding,padding), 'This is a test.', font=font, file=255)
	img.save('test.png')
	b = time.time()
