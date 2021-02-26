#/usr/bin/env python3


import treepoem
import sys

if len(sys.argv)<2:
	print('error: supply  content arg.')

image = treepoem.generate_barcode(
	barcode_type='azteccode',
	data=sys.argv[1]
)
image.convert('1').save('/home/pi/barcodes/'+sys.argv[1]+'.png')

