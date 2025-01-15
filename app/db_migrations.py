import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
a = cur.execute("select * from IceCreamSize where flavor_id = 2;").fetchall()
print(a)
