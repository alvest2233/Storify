import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="password"
)

mycursor = mydb.cursor()

print("Welcome to Storify!")
print("Type 1 if you have an existing database you would like to access")
print("Type 2 if you would like to create or deleted a database")
dbChoice = input("Type here: ")

if dbChoice == '1':
   print("You choose that you would like to open an existing database please wait...")
   dbAlter = input("Type here: ")
elif dbChoice == '2':
   print("Type 1 to create a database")
   print("Type 2 to delete a database")
   dbAlter = input("Type here: ")
   
   if dbAlter == '1':
       print("")
   elif dbAlter == '2':
       print("")
       mycursor.execute("SHOW DATABASES")
       for x in mycursor:
          print(x)

## mycursor.execute("CREATE DATABASE mydatabase")


