from app.database.db import get_connection

# open a connection to the database
conn = get_connection()

# create a cursor to execute SQL queries
cursor = conn.cursor()

# retrieve all rows from customers table
cursor.execute("SELECT * FROM customers")

rows = cursor.fetchall()

# print results
for row in rows:
    print(row)

# clean up resources
cursor.close()
conn.close()