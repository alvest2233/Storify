print("hello world")

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="3b1wtesting"
)

print(mydb)
