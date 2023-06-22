import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO movies (title, content) VALUES (?, ?)",
               ('First Movie', 'Desc1')
               )

cursor.execute("INSERT INTO movies (title, content) VALUES (?, ?)",
               ('Second Movie', 'Desc2')
               )

connection.commit()
connection.close()
