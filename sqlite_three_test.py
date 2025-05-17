import sqlite3

conn:sqlite3.Connection = sqlite3.connect("patients.db")


cursor = conn.cursor()
cursor.execute("SELECT * FROM patients")
column_names = [description[0] for description in cursor.description]

print("Column names:", column_names)
rows = cursor.fetchall()
result = {}
for row in rows:
    result[row[0]] = dict(zip(column_names,row))

print(result)

