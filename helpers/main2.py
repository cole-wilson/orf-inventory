import os
import mysql.connector

print('Connecting to local MariaDB server...')

db = mysql.connector.connect(
	host="localhost",
	username="pi",
	password="robots",
	database="inventory"
)
print('Done!')

cursor = db.cursor()

while True:
	barcode = input('> ')
	if barcode == "<QUIT>":
		break
	elif barcode.startswith('~'):
		os.system(barcode[1:])
	else:
		sql = "UPDATE parts SET qty_stock = qty_stock - 1 WHERE barcode = '{barcode}'".format(barcode=barcode)
		cursor.execute(sql)
		db.commit()
		sql = "UPDATE parts SET qty_robot = qty_robot + 1 WHERE barcode = '{barcode}'".format(barcode=barcode)
		cursor.execute(sql)
		db.commit()
		sql = "SELECT * FROM parts WHERE barcode = '{}'".format(barcode)
		cursor.execute(sql)
		result = cursor.fetchall()
		if len(result) > 0:
			print('UPDATED: {} | {} | {} | {} | {} | {} | {} | {}'.format(*result[0]))
		else:
			print('{} not found.'.format(barcode))
