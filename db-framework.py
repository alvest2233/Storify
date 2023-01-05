import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="password"
)

mycursor = mydb.cursor()
t = True
##Function to show the database
def showDataBase():
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    filteredx = str(x)
    ## parses list of database names to remove illegal punction
    ## this reduces user confusion
    a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    print(a)
    print("")

def addColumn(tableName, columnName, listOfValues):
    ## UNTESTED CODE
    ## Takes table name, desired new columnName, and created values in list format with commas between
    column = "INSERT INTO {} ({}) VALUES ({})"

    mycursor.execute(column.format(tableName, columnName, listOfValues))
    print("Change committed")
    mydb.commit()

def findRow(tableName, columnName, value):
  ##NOT DONE 
    sql = "SELECT * FROM customers WHERE address ='Park Lane 38'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
def delete(tableName, condition):
    ## UNTESTED CODE
    ## Takes table name, desired new columnName, and created values in list format with commas between
    column = "DELETE FROM {} WHERE {}"

    mycursor.execute(column.format(tableName, condition))
    print("Change committed")
    mydb.commit()    

def update(tableName, setValue, changeValue, whereValue, whereCondition):
    sql = "UPDATE {} SET {} = {} WHERE {} = {}"

    mycursor.execute(sql)## NOTTTTTTTTT DONNNNNNNNNEEEEEEEEEEE OHMM WAS HERE

while t==True:
    print("Welcome to Storify!")
    print("Type 1 if you have an existing database you would like to access")
    print("Type 2 if you would like to create or deleted a database")
    dbChoice = input("Type here: ")
    ##checking input from user to see if they want to create/delete a database or open an existing one
    if dbChoice == '1':
      print("You choose that you would like to open an existing database please wait...")
      showDataBase()
      dbFileName = input("Type file name: ")

      userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
      if userEnd=='1':
        continue
      elif userEnd=='2':
        t=False
    
    elif dbChoice == '2':
      print("Type 1 to create a database")


      
      print("Type 2 to delete a database")
      dbAlter = input("Type here: ")
      
      if dbAlter == '1':
        ## creating new database

        showDataBase()

            ## gets user input for db name and then creates database
        print("Please type in the name of your new, desired database")
        dbAdd = input("Type here: ")
          
        addCmd = ("CREATE DATABASE {};")
        mycursor.execute(addCmd.format(dbAdd))
        print("Change committed")
        mydb.commit()
        
        userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
        if userEnd=='1':
          continue
        elif userEnd=='2':
          t=False

      elif dbAlter == '2':
          showDataBase()

          print("Please type the name of the database you would like to delete:")
          dbDel = input("Type here: ")
          
          dropCmd = ("DROP DATABASE {};")
          mycursor.execute(dropCmd.format(dbDel))
          print("Change committed")
          mydb.commit()
          
          userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
          if userEnd=='1':
            continue
          elif userEnd=='2':
            t=False


          

      ## mycursor.execute("CREATE DATABASE mydatabase")


