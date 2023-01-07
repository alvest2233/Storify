#from 3b1wDBclasses import * 
# # TO FIX: separate function file
import mysql.connector
from prettytable import PrettyTable

mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="password"
)

mycursor = mydb.cursor(buffered=True)
t = True
# Function to show the database
def showDataBase():
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    filteredx = str(x)
    # parses list of database names to remove illegal punction
    # this reduces user confusion
    a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    print(a)
    print("")

"""def addColumn(tableName, columnName, listOfValues):
    # UNTESTED CODE
    # Takes table name, desired new columnName, and created values in list format with commas between
    column = "INSERT INTO {} ({}) VALUES ({})"

    mycursor.execute(column.format(tableName, columnName, listOfValues))
    print("Change committed")
    mydb.commit()"""

def columnManip(tableName, columnName, inputNum):
    # If user inputs 1, add a new column with a name of their choice
    if inputNum == '1':
      addC = "ALTER TABLE {} ADD {} VARCHAR(255)"
      mycursor.execute(addC.format(tableName, columnName))
      print("Change committed")
      mydb.commit()
    # If user inputs 2, drop the column based on its name 
    elif inputNum == '2':
      dropC = "ALTER TABLE {} DROP COLUMN {}"
      mycursor.execute(dropC.format(tableName, columnName))
      print("Change committed")
      mydb.commit()
    # If user inputs anything else other than 1 or 2, modify the column based on the name
    else:
      modC = "ALTER TABLE {} MODIFY COLUMN {} VARCHAR(255)"
      mycursor.execute(modC.format(tableName, columnName))
      print("Change committed")
      mydb.commit()

def numCol(DBName, tableName):
    numC = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '{}' AND table_name = '{}'"
    mycursor.execute(numC.format(DBName, tableName))
    col = mycursor.fetchall()
    mydb.commit()
    for x in col:
      return x

def colName(tableName):
    cName = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS where table_name = '{}'"
    mycursor.execute(cName.format(tableName))
    col = mycursor.fetchall()
    mydb.commit()
    return col

def addRow(tableName, rowName, listOfValues):
    # UNTESTED CODE
    '''row = "INSERT INTO %s (ohm, tiago) VALUES (%s, %s)"
    values = (tableName, rowName, listOfValues)
    print(tableName, rowName, listOfValues)
    print(row.format(tableName, rowName, listOfValues))
    mycursor.execute(row, values)
    print("Change committed")
    mydb.commit()'''
    mycursor.execute("INSERT INTO sridhar (ohm, tiago) VALUES ('value1', 'value2')")
    mydb.commit()

def delRow(tableName, columnName, value):
    dRow = "DELETE FROM {} WHERE {} = {}"
    mycursor.execute(dRow.format(tableName, columnName, value))
    mydb.commit()
    print("Row has been removed")

def findRow(tableName, columnName, value):
    # UNTESTED CODE
    # Finding the row which meets the criteria
    sql = "SELECT {} FROM {} WHERE {} = {}"
    mycursor.execute(sql.format(columnName, tableName, columnName, value))
    myresult = mycursor.fetchall()
    for x in myresult:
      print(x)
    
'''def delete(tableName, condition):
    #  UNTESTED CODE
    # Takes table name, desired new columnName, and created values in list format with commas between
    column = "DELETE FROM {} WHERE {}"

    mycursor.execute(column.format(tableName, condition))
    print("Change committed")
    mydb.commit()'''    

def update(tableName, columnValue, changeValue, columnName, whereCondition):
    # Takes table name, desired set value, the value it will be changed to, the condition for the change and what the condition will apply to 
    sql = "UPDATE {} SET {} = {} WHERE {} = {}"
    
    # Take the given parameters and input them into the right position
    mycursor.execute(sql.format(tableName, columnValue, changeValue, columnName, whereCondition))
    print("Change committed")
    mydb.commit()
    
def showAllDBTables(dbName):
  # accepts the desired database name 
  tables = "SHOW TABLES IN {}"
  try:
     mycursor.execute(tables.format(dbName))
     mydb.commit()
  except:
    print("Table preview unavailable, no tables currently exist in the DB")
  print("Change committed")
  
''' ###ORIGINAL###
def showFromTable(tableName):
    table = "SELECT * FROM {}"
    try:
      mycursor.execute(table.format(tableName))
      mydb.commit()
    except:
      print("Table preview unavailable, no data currently exists in the table")
    print("Change committed")
'''
'''###TRY NUMBER 2###
def showFromTable(tableName):
  table = "SELECT * FROM {}"
  mycursor.execute(table.format(tableName))
  try:
    rows = mycursor.fetchall()
    for row in rows:
      for col in row:
        print (col, row = ' ')   
      print()
  except:
    print("ERROR : THE TABLE COULD NOT PRINT")
'''


'''
def showFromTable(tableName):
  displayDB = PrettyTable()
  try:
    showCols = "SHOW COLUMNS FROM {}"
    cols = mycursor.execute(showCols.format(tableName))
    print(cols)  
    mydb.commit()
    displayDB.field_names = [cols]
    
    table = "SELECT * FROM {}"
    mycursor.execute(table.format(tableName))  
    mydb.commit()
    results = mycursor.fetchall()

    for x in results:
      displayDB.add_column(x)  
    
    print(displayDB)
  except:
    print("ERROR: TABLE COULD NOT PRINT PLEASE TRY AGAIN LATER")
'''

def showFromTable(tableName):
    table = "DESCRIBE {}"
    try:
      mycursor.execute(table.format(tableName))
      mydb.commit()
    except:
      print("Table preview unavailable, no data currently exists in the table")
    print("Change committed")

def dropTable(dbChosen, tableName):
    validTables = "SHOW TABLES IN {}"
    try:
      mycursor.execute(validTables.format(dbChosen))
      mydb.commit()

      tableList = []
      for x in mycursor:
        filteredx = str(x)
        a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        tableList.append(a)

      print(tableList)
      
      if tableName in tableList:
        deleteTableScript = "DROP TABLE {}"
        mycursor.execute(deleteTableScript.format(tableName))
        mydb.commit()
        print("Table {} has been dropped".format(tableName))
      else:
        print("Table does not exist, and cannot be deleted.")  
    except:
      print("There are no valid databases. Please create a DB first")


  
#######################AARYA###########################OHM###################NOT#TIAGO####################SRIDHAR#####################################


print("Welcome to Storify!")
# loop used to ensure that the user can use the program over again until they want to exit
while t:
    # print statements
    print("Type 1 if you have an existing database you would like to access")
    print("Type 2 if you would like to create or delete a database")
    print("Type 3 to exit the program")
    #user input

    while True:
      dbChoice = input("Type here: ")

      if dbChoice == '1' or dbChoice == '2' or dbChoice == '3':
        break
      else:
        print("The input entered in incorrect, please type in the right value")



    # checking input from user to see if they want to create/delete a database or open an existing one
    while dbChoice == '1':
      # showing pre-existing list of databases
      print("You choose that you would like to open an existing database please wait...")
      
      
      # prompts user for DB holding desired table, shows tables in DB
      showDataBase()
      print("Please list the database your table is located in:")
      dbChosen = input("Selected database: ")
      
      useDB = "USE {}"
      mycursor.execute(useDB.format(dbChosen))

      # OPTIONS FOR ACCESSING / CREATING TABLE

      tableLoop = True
      while tableLoop == True:
        print("Type 1 if you have an existing table you would like to access")
        print("Type 2 if you would like to create a table")
        print("Type 3 if you would like to delete a table")
        print("Type 4 if you would like to return")
        tableChoice = input()
        
        # if user has a table already made, they can go on to modify it
        if tableChoice == '1':
          tableLoop = False
        
        elif tableChoice == '2':
          # TO DO USER SHOULD BE ABLE TO CHOOSE 
          print("Input the name of the table")
          newTN = input()
          print("Enter first column name")
          firstC = input()
          print("Enter second column name")
          secondC = input()
          
          createTableScript = "CREATE TABLE {} ({} VARCHAR(255), {} VARCHAR(255))"
          mycursor.execute(createTableScript.format(newTN, firstC, secondC))

          tableLoop = False
          
        elif tableChoice == '3':
          print("Enter the name of the table you would like to delete")
          tableName = input()
          dropTable(dbChosen, tableName)

          tableLoop = False
        elif tableChoice == '4':  
            break 
            dbChoice = '0'
            
      if tableChoice == '4':
        break






















      # prompts user for desired table, sends to table modification loop
      showAllDBTables(dbChosen)
      print("Please state the table you would like to access:")
      dbTableName = input("Type table name: ")
      tableModLoop = True
    
      # table modification loop, shows current table, prompts user for change then breaks off into chosen options
      while tableModLoop: 
        showFromTable(dbTableName)
        numberC = numCol(dbChosen, dbTableName)
        colNames = colName(dbTableName)
        colNameList = []
        i = 0
        while i < numberC[0]:
          colNameList.insert(i, colNames[i][3])
          i = i + 1
        print(colNameList)
        
        updateBool = False
        rowBool = False
        columnBool = False
        
        print("Type 1 to change a single cell")
        print("Type 2 to change a row")
        print("Type 3 to change a column")
        print("Type 4 to exit the program or return to the previous options")
        dbModChoice = input()
        
        if dbModChoice == '1':
          updateBool = True
        elif dbModChoice == '2':
          rowBool = True
        elif dbModChoice == '3':
          columnBool = True
        elif dbModChoice == '4':
          tableModLoop = False
          dbChoice = '0'
        
        #################################################################################
        
        # Single cell replacement user prompts, inputs sent to single cell update method
        while updateBool:
          print("What is the name of the cell's column?")
          cellColumn = input()
          print("What is the unique index's column name?")
          cellIndex = input()
          print("What is the unique index number of the cell?")
          cellLocation = input()
          print("What would you like the new cell value to be?")
          cellValue = input()
          update(dbTableName,cellColumn,cellValue,cellIndex,cellLocation)
          updateBool = False

        ######################################################

        # Row manipulation, prompts user for adding row, removing row, or finding a desired row
        while rowBool:
          print("Type 1 to add a row from the table")
          print("Type 2 to remove a row from the table")
          print("Type 3 to find your desired row")
          print("Type 4 to return/exit")
          rowModChoice = input()

          # Ask user for the values they would like to add to the new row and display the new row after
          if rowModChoice == '1':
            print("Please enter the column name(s) you would like value entered into for the row (seperate each name with a comma)")   
            columnName = input()
            print("List the values you would like to add based on the columns you mentioned before (seperate each value with a comma)")
            values = input()
            
            addRow(dbTableName, columnName, values)
            rowBool = False
          
          elif rowModChoice == '2':
            print("Please enter the column name where that value exists")
            columnName = input()
            print("Please enter a value that exists in the row currently")   
            value = input()
            
            delRow(dbTableName, columnName, value)
            rowBool = False

          elif rowModChoice == '3':
            print("Please enter the column where that value exists")
            columnName = input()
            print("Please enter the value you are searching for")
            value = input()
            
            findRow(dbTableName, columnName, value)
            rowBool = False
            
          elif rowModChoice == '4':
            rowBool = False

        ######################################################
        # Column manipulation which allows user to add column, remove column, or change column name
        while columnBool:
          print("Type the column you would like to manipulate")
          colNum = input()

          # Getting the user input
          print("Type 1 to add column to table")
          print("Type 2 to remove column from table")
          print("Type 3 to change a column name")
          print("Type 4 to return/exit")
          inputNum = input()

          if input == 4:
            columnBool = False

          columnManip(dbTableName, colNum, inputNum)
          columnBool = False
        ######################################################
        # Return to main selection screen
        if dbModChoice == '4':
          tableModLoop = False
 
    ##if user picks 2, ask if user wants to create or delete a database, get user input
    while dbChoice == '2':
      print("Type 1 to create a database")
      print("Type 2 to delete a database")
      dbAlter = input("Type here: ")
      ##
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
          dbChoice='0'
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
            dbChoice='0'
          elif userEnd=='2':
            t=False
    ## Triggers boolean to exit main program loop if user chooses to exit program   
    while dbChoice == '3':
      t = False


