import sqlite3

connection = sqlite3.connect('../resource/test.db')
cur = connection.cursor()
cur.execute('INSERT INTO foo (o_id, fruit, veges) VALUES(NULL, "apple", "broccoli")')
connection.commit()
print cur.lastrowid
cur.execute('SELECT * FROM foo')
print cur.fetchall()



