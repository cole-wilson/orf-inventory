#/usr/bin/env python3
import sys
import os

printername = open('printerloc').read().split('\n')[0]
zpl = """^xa
^fo45,30
^boN,7,N,101,N
^fd{b}^fs

^fo0,145
^AAN,15
^FB203,2,0,C,0
^fd{c}-{b}\&^fs

^fo0,165
^AAN,10
^FB203,2,0,C,0
^fd{n}\&^fs

^xz"""
def make_barcode(data):
    return
    data = str(data)
    image = treepoem.generate_barcode(
            barcode_type='azteccode',
    	    data=data
    )
    return image.convert('1')

def make_zpl(data):
    return
    image = make_barcode(data).resize((5,5))
    label = zpl.Label(100,60)
    label.origin((label.width-image.width)/2, 0)
    label.write_graphic(image,image.width)
    label.endorigin()
    return label.dumpZPL()

def print_label(barcode,name,category):
    os.system('echo \'{zpl}\' > {printername}'.format(
        printername=printername,
	zpl=zpl.format(
        b=barcode,
        n=name,
        c=category
    )))

if __name__ == '__main__':
    print_label('This is a test...',"Test","T")
