import mysql.connector
import re

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
##checking input from user to see if they want to create/delete a database or open an existing one
if dbChoice == '1':
   print("You choose that you would like to open an existing database please wait...")
   mycursor.execute("SHOW DATABASES")
   for y in mycursor:
      print(y)

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
        filteredx = str(x)
        ## parses list of database names to remove illegal punction
        ## this reduces user confusion
        a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        print(a)
       print("")

       print("Please type the name of the database you would like to delete:")
       dbDel = input("Type here: ")
       
       dropCmd = ("DROP DATABASE {};")
       mycursor.execute(dropCmd.format(dbDel))
       print("Change committed")
       mydb.commit()


       

## mycursor.execute("CREATE DATABASE mydatabase")


