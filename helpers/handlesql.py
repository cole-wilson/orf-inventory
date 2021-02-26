import os
import sys
import mysql.connector
from prettytable import PrettyTable

#try:
db = mysql.connector.connect(
        username="pi",
        password="robots",
        database="replicator"
)
#except:
#    print('Error connecting to mariadb server')
#    sys.exit(99)

cursor = db.cursor(buffered=True)

def handlesql(inp):
    if inp != "":
        try:
            cursor.execute(inp)
            db.commit()
            a = cursor.fetchall()
            table = PrettyTable()
            table.field_names = [i[0] for i in cursor.description]
            table.add_rows(a)
            print('\n')
            print(table)
        except mysql.connector.Error as err:
            print('Error: {}'.format(err))
