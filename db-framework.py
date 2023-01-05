print("hello world")

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="password"
)

print(mydb)
