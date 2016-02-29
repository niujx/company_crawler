import sqlite3

connection = sqlite3.connect('/db/test.db3')
cur = connection.cursor()
cur.execute('CREATE TABLE foo (o_id INTEGER PRIMARY KEY, fruit VARCHAR(20), veges VARCHAR(30))')
connection.commit()
cur.execute('INSERT INTO foo (o_id, fruit, veges) VALUES(NULL, "apple", "broccoli")')
connection.commit()
print cur.lastrowid
cur.execute('SELECT * FROM foo')
print cur.fetchall()



