import os
import sys
import mysql.connector
from helpers.OLED import OLED

db = mysql.connector.connect(
        username="pi",
        password="robots",
        database="replicator"
)

cursor = db.cursor(buffered=True)

def handlebarcode(barcode, source, destination, cmode):
    if barcode != "":
        try:
            sql = "UPDATE items SET qty_{d} = qty_{d} + 1, qty_{s} = qty_{s} - 1 WHERE item_num = '{b}'"
            cursor.execute(sql.format(s=source, d=destination, b=barcode))
            sql = "SELECT item_name, qty_stock, qty_robot, qty_testing FROM items WHERE item_num = '{}'".format(barcode)
            cursor.execute(sql)
            name, stock, robot, testing = cursor.fetchall()[0]
            db.commit()
            print('(scan) moved one "{}" (barcode {}) from source {} to destination {}'\
                  '\t\tIn Stock: {}\t\tOn Robot: {}\t\tIn Testing: {}'.format(name, barcode, source, destination,
                      stock, robot, testing
                  ))
            OLED(mode=cmode,source=source,destination=destination,message=[
                ""+name,
            ])
        except IndexError:
            print(barcode, 'not found!')
        except mysql.connector.Error as err:
             pass
