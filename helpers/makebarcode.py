#/usr/bin/env python3

import treepoem
import sys

def make_barcode(data):
    data = str(data)
    image = treepoem.generate_barcode(
            barcode_type='azteccode',
    	    data=data
    )
    image.convert('1').save('/home/pi/barcodes/'+data+'.png')

if __name__ == '__main__':
    make_barcode(sys.argv[2])
