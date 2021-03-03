import os
import sys
import mysql.connector
import blessed
import keyboard
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
		sys.exit(876)
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
	validsuppliers = ["NEW"]
	for abbreviation, name in cursor.fetchall():
		validsuppliers.append(abbreviation)
		print('{}: {}'.format(abbreviation, name))
	print('NEW: Create a new supplier')
	while True:
		itemsupplier = input('Choose a supplier from the above list > ').upper()
		if itemsupplier not in validsuppliers:
			print('That is not a valid option.')
		else:
			break
	if itemsupplier == 'NEW':
		while True:
			try:
				itemsupplier = input('New supplier abbreviation > ').upper()
				assert len(itemsupplier) == 3, "Length of abbreviation must be exactly three chars long."
				assert itemsupplier != "NEW", "Supplier abbreviation must not be `NEW`!"
				assert itemsupplier not in validsuppliers, "Abbreviation already exists!"
				break
			except AssertionError as err:
				print('Error: {}'.format(err))
		newname = input('New supplier name > ')
		cursor.execute("INSERT INTO suppliers SET supp_abbr = '{}', supp_name = '{}'".format(itemsupplier,newname))
	# Get cost
	while True:
		itemcost = input('Cost of part > ')
		try:
			itemcost = float(itemcost)
			break
		except:
			print('That is not a valid cost.')
	# Get part number
	partnum = input("Supplier Part Number > ")
	if len(partnum) > 12:
		partnum = partnum[:12]

	# get qty
	try:
		qty_stock = int(input('Quantity in stock [blank for 0] > '))
	except:
		qty_stock = 0
	qty_robot = 0
	qty_testing = 0

	try:
		sql = "INSERT INTO items VALUES ('{}',NULL,'{}','{}','{}',{},{},{},{})".format(itemcategory,itemname,itemsupplier,partnum,itemcost,qty_stock,qty_robot,qty_testing)
		cursor.execute(sql)
		db.commit()
		sql = "SELECT item_num FROM items"
		cursor.execute(sql)
		barcode = cursor.fetchall()[-1][0]
		db.commit()
		handlesql("SELECT * from items")
		print("Added!")
		while True:
			if qty_stock < 5:
				numprint = qty_stock
				break
			numprint = input('How many barcodes should I print? [blank for {}] > '.format(qty_stock))
			if numprint == '':
				numprint = qty_stock
				break
			try:
				numprint = int(numprint)
				assert numprint > 0
				break
			except:
				print('That is not a valid number!')
		print('Printing...')
		for x in range(numprint):
			print_label(barcode)
		print('To print more barcodes, run /barcode.')
	except mysql.connector.Error as err:
		pass
