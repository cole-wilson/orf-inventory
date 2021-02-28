import os
import sys
import mysql.connector
import blessed
from helpers.handlesql import handlesql
from helpers.makebarcode import print_label
term = blessed.Terminal()  # For colored output
db = mysql.connector.connect(
	username="pi",
	password="robots",
	database="replicator"
)
cursor = db.cursor(buffered=True)

def coloredinput(i):
	i = input(term.green(i))
	if i == '/quit':
		sys.exit(0)
	else:
		return i

def coloredprint(*args):
	return print(term.purple(" ".join(args)))

def handleadd(itemname):
	input = coloredinput
	print = coloredprint
	if itemname == '':
		print('')
		return
	if len(itemname) > 44:
		itemname = itemname[:44]

	# Get Category ================
	cursor.execute("SELECT * FROM categories")
	validabrevs = []
	for abbreviation, name in cursor.fetchall():
		validabrevs.append(abbreviation)
		print('{}: {}'.format(abbreviation, name))
	while True:
		itemcategory = input('Choose a category from the above list > ').upper()
		if itemcategory not in validabrevs:
			print('That is not a valid option.')
		else:
			break

	# Get Supplier ================
	cursor.execute("SELECT * FROM suppliers")
	validsuppliers = []
	for abbreviation, name in cursor.fetchall():
		validsuppliers.append(abbreviation)
		print('{}: {}'.format(abbreviation, name))
	while True:
		itemsupplier = input('Choose a supplier from the above list > ').upper()
		if itemsupplier not in validsuppliers:
			print('That is not a valid option.')
		else:
			break
	# Get cost
	while True:
		itemcost = input('Cost of part > ')
		try:
			itemcost = float(itemcost)
			break
		except:
			print('That is not a valid cost.')
	# Get part number
	partnum = input("Part Number > ")
	if len(partnum) > 12:
		partnum = partnum[:12]

	# get qty
	try:
		qty_stock = int(input('Quantity in stock [blank for 0] > '))
	except:
		qty_stock = 0

	try:
		qty_robot = int(input('Quantity on robot [blank for 0] > '))
	except:
		qty_robot = 0

	try:
		qty_testing = int(input('Quantity in testing [blank for 0] > '))
	except:
		qty_testing = 0

	try:
		sql = "INSERT INTO items VALUES ('{}',NULL,'{}','{}','{}',{},{},{},{})".format(itemcategory,itemname,itemsupplier,partnum,itemcost,qty_stock,qty_robot,qty_testing)
		cursor.execute(sql)
		sql = "SELECT item_num FROM items"
		cursor.execute(sql)
		barcode = cursor.fetchall()[-1][0]
		db.commit()
		handlesql("SELECT * from items")
		print("Added!")
		print('Printing label ({}) ...'.format(barcode))
		print_label(barcode)
	except mysql.connector.Error as err:
		pass
