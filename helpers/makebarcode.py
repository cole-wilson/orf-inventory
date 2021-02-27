#/usr/bin/env python3

import treepoem
import sys
import zpl
import os

printername = open('printerloc').read().split('\n')[0]

def make_barcode(data):
    data = str(data)
    image = treepoem.generate_barcode(
            barcode_type='azteccode',
    	    data=data
    )
    return image.convert('1')

def make_zpl(data):
    image = make_barcode(data).resize((5,5))
    label = zpl.Label(100,60)
    label.origin((label.width-image.width)/2, 0)
    label.write_graphic(image,image.width)
    label.endorigin()
    return label.dumpZPL()

def print_label(data):
    os.system('echo "^xa^fo50,50^boN,3,N,205,N^fd{barcode}^fs^fo50,165^A0,10,20^fd{barcode}^fs^xz" > {printername}'.format(
        printername=printername,
        barcode=data
    ))

if __name__ == '__main__':
    print_label('This is a test...')
