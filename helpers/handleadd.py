import os
import sys
import mysql.connector

db = mysql.connector.connect(
        username="pi",
        password="robots",
        database="replicator"
)

cursor = db.cursor(buffered=True)

def handlebarcode(itemname):
    if itemname == '':
        print('')
        return

    while True:
        category = input('')

    try:
        sql = "SELECT item_name, qty_stock, qty_robot, qty_testing FROM items WHERE item_num = '{}'".format(itemname)
        cursor.execute(sql)
        name, stock, robot, testing = cursor.fetchall()[0]
        db.commit()
        print('(scan) moved one "{}" (barcode {}) from source {} to destination {}'\
              '\t\tIn Stock: {}\t\tOn Robot: {}\t\tIn Testing: {}'.format(name, barcode, source, destination,
                  stock, robot, testing
              ))
    except IndexError:
        print(barcode, 'not found!')
    except mysql.connector.Error as err:
        pass
