import sqlite3

# Connect to the old and new databases
conn_old = sqlite3.connect('old_database.db')
conn_new = sqlite3.connect('db/database.db')
cur_old = conn_old.cursor()
cur_new = conn_new.cursor()


old_flavors = cur_new.execute("SELECT * FROM BillItems;").fetchall()
print(old_flavors)