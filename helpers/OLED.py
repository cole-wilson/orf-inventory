from PIL import Image

def OLED(source=None,destination=None):
	img = Image.new('RGB', (100,100), 'red')
	img.save('test.png')
