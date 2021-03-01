import os
import sys
import mysql.connector
from prettytable import PrettyTable
import blessed
import time

term = blessed.Terminal()
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

def complete(text, state):
	cursor.execute('SELECT items.item_name, suppliers.sup_abbr FROM items, suppliers')
	names = map(str,list(sum(cursor.fetchall(),())))
#	names = []
	sql_keywords = ['SELECT','INSERT','WHERE','INTO','VALUES','ORDER','FROM']
	files = os.listdir('.')
	commands = ['quit','?','.','mode']
	all = [*names,*sql_keywords,*files,*commands]
	all = [x+" " for x in all if x.upper().startswith(text.upper())] + [None]
	return all[state]
#complete('',0)
def handlesql(inp):
    if inp != "":
        try:
            cursor.execute(inp)
            db.commit()
            a = cursor.fetchall()
            table = PrettyTable()
            table.field_names = [i[0] for i in cursor.description]
            table.add_rows(a)
            print('\n')# + term.purple)
            print(table)
            #print(term.normal)
        except mysql.connector.Error as err:
            print('Error: {}'.format(err))
