print("hello world")

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="3b1wtesting"
)

print(mydb)
