#from 3b1wDBclasses import * 
# # TO FIX: separate function file
import mysql.connector
from functions import *
from prettytable import PrettyTable


mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="password"
)

mycursor = mydb.cursor(buffered=True)
t = True
createTableLoop = True

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

def columnAdd(tableName, columnName, afterCol, colNames):
    # Add a new column with a name of their choice

    while columnName not in colNames:
      addC = "ALTER TABLE {} ADD {} VARCHAR(255) NOT NULL AFTER {}"
      mycursor.execute(addC.format(tableName, columnName,afterCol))
      print("Change committed")
      mydb.commit()
    while columnName in colNames:
      print("Error: Column name already in use. Please try a different name")
      columnName = input("Type new column name here:")
      
    
def columnChange(tableName, columnName, newCol, colNameList):
    # Modify the column based on the name
    innerLoop = True
    outerLoop = True
    while outerLoop:
      for x in colNameList:
        if x == newCol:
          innerLoop = False
      if innerLoop == False:
        print("The name you entered already exists. Please choose new column name to change into: ")
        innerLoop = True
        newCol = input()
      else:
        outerLoop = False
        
    modC = "ALTER TABLE `{}` RENAME COLUMN {} TO {}"
    mycursor.execute(modC.format(tableName, columnName, newCol))
    print("Change committed")
    mydb.commit()

def columnRemove(tableName, columnName, colNames):
    # Drop the column based on its name 
    while columnName in colNames:
      dropC = "ALTER TABLE {} DROP COLUMN {}"
      mycursor.execute(dropC.format(tableName, columnName))
      print("Change committed")
      mydb.commit()
    while columnName not in colNames:
      print("ERROR: The column name that was entered does not exit, please enter a name that exists in the table")
      columnName = input("Type new column name here:")

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

def addRow(tableName, numCol, colNames):
    columns = "("
    between = ", "
    i = 0
    while i < numCol:
      columns = "".join([columns, colNames[i]])
      columns = "".join([columns, between])
      i = i + 1
    columns = columns[:-2]
    columns = "".join([columns, ")"])

    i = 0
    inputs = []
    prompt = "Please input the value for the column "
    while i < numCol:
        tempVar = "".join([prompt, colNames[i]])
        print("".join([tempVar, ":"]))
        answer = input()
        inputs.insert(i, answer)
        i = i + 1
    x = str(inputs)
    x = x.replace("[", "(").replace("]", ")")
    
    test = ("INSERT INTO {} {} VALUES {}")
    mycursor.execute(test.format(tableName, columns, x))
    print("Change committed")
    mydb.commit()

def delRow(tableName, numCol, colNames):
    test = False
    innerTest = False
    while test == False:
      try:
        prompt = "Please enter the name of the unique index column: "
        columns = "("
        between = ", "
        i = 0
        while i < numCol:
          columns = "".join([columns, colNames[i]])
          columns = "".join([columns, between])
          i = i + 1
        columns = columns[:-2]
        columns = "".join([columns, ")"])
        print("".join([prompt, columns]))
        columnName = input()
        print("Please enter the unique index of the row you would like to delete: ")   
        value = input()
        
        existCheck = "SELECT {} FROM {}"
        mycursor.execute(existCheck.format(columnName, tableName))
        myresult = mycursor.fetchall()
        tableList = []
        for x in myresult:
          myresult = str(x)
          a = myresult.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
          tableList.append(a)
        for x in tableList:
          if value == x:
            innerTest = True
        
        if innerTest:
          dRow = "DELETE FROM {} WHERE {} = '{}'"
          mycursor.execute(dRow.format(tableName, columnName, value))
          mydb.commit()
          print("Row has been removed")
          test = True
        else:
          innerTest = False
          print("The row does not exist. Please try again and make sure the correct information is entered.")
      except:
        print("The row does not exist. Please try again and make sure the correct information is entered.")

def findRow(tableName, numCol, colNames):
    # UNTESTED CODE
    # Finding the row which meets the criteria
    test = False
    innerTest = False
    while test == False:
      try:
        prompt = "Please enter the name of the unique index column: "
        columns = "("
        between = ", "
        i = 0
        while i < numCol:
          columns = "".join([columns, colNames[i]])
          columns = "".join([columns, between])
          i = i + 1
        columns = columns[:-2]
        columns = "".join([columns, ")"])
        print("".join([prompt, columns]))
        columnName = input()
        print("Please enter the unique index of the row you would like to find: ")   
        value = input()

        existCheck = "SELECT {} FROM {}"
        mycursor.execute(existCheck.format(columnName, tableName))
        myresult = mycursor.fetchall()
        mydb.commit()
        tableList = []
        for x in myresult:
          myresult = str(x)
          a = myresult.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
          tableList.append(a)
        for x in tableList:
          if value == x:
            innerTest = True
        
        if innerTest:
          fRow = "SELECT * FROM {} WHERE {} = '{}'"
          mycursor.execute(fRow.format(tableName, columnName, value))
          result = mycursor.fetchall()
          mydb.commit()
          
          test = True
        else:
          innerTest = False
          print("The row does not exist. Please try again and make sure the correct information is entered.")
      except:
        print("The row does not exist. Please try again and make sure the correct information is entered.")
      
      searchResults = "\nResults found for {} = '{}':"
      print(searchResults.format(columnName, value)) 
      displayDB = PrettyTable()
      displayDB.field_names = colNames
      try:
        for x in result:
          displayDB.add_row(x)  
        print(displayDB)
        print ("\n")
      except:
        print("ERROR: TABLE COULD NOT PRINT PLEASE TRY AGAIN LATER")
    
'''def delete(tableName, condition):
    #  UNTESTED CODE
    # Takes table name, desired new columnName, and created values in list format with commas between
    column = "DELETE FROM {} WHERE {}"

    mycursor.execute(column.format(tableName, condition))
    print("Change committed")
    mydb.commit()'''    

def update(tableName, columnValue, changeValue, columnName, whereCondition):
  # Takes table name, desired set value, the value it will be changed to, the condition for the change and what the condition will apply to 
  sql = "UPDATE {} SET {} = '{}' WHERE {} = '{}'"
  
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
  
def showFromTable(columnNameList, tableName):
  displayDB = PrettyTable()
  
  displayDB.field_names = columnNameList

  try:
    table = "SELECT * FROM {}"
    mycursor.execute(table.format(tableName))  
    results = mycursor.fetchall()
    mydb.commit()

    for x in results:
      displayDB.add_row(x)  
    
    print(displayDB)
    print ("\n")
  except:
    print("ERROR: TABLE COULD NOT PRINT PLEASE TRY AGAIN LATER")

def createTable():
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
      
  except:
      print("There are no valid databases. Please create a DB first")
      
  while True:
    print("Input the name of the table. Please use a unique name")
    newTN = input()

    if newTN not in tableList:
      print("Enter the number of columns you would like to have")

      while True:
        try:
          numColumns = int(input())
          break
        except:
          print("ERROR: Please try again and enter a number value")
          
      numColumns = (int)(numColumns)
      colNames = []
      createTableScript = "CREATE TABLE {} ("
      
      for i in range(numColumns):
        colPrompt = "Enter name for column {}"
        index = i + 1
        print(colPrompt.format(index))
        temp = input()
        colNames.append(temp)
        if i == (numColumns - 1):
          createTableScript += (colNames[i] + " VARCHAR(255))")
        else:
          createTableScript += (colNames[i] + " VARCHAR(255), ")  
        
      try:
        mycursor.execute(createTableScript.format(newTN))
        mydb.commit()
      except:
        print("ERROR: TABLE UNABLE TO BE CREATED")
      break 
        
    elif newTN in tableList:
      print("Table name already in use, and cannot be created")
  
  ##print("Input a new name for the table. Please use a unique name")
  ##newTN = input()  

  ## NO REPROMPT, OHM WILL GET THIS LOOPING BACK TO 1234 MENU INSTEAD OF REPROMPTING

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

def addDB(dbName):

  mycursor.execute("SHOW DATABASES")
  mydb.commit()

  dbList = []
  for x in mycursor:
    filteredx = str(x)
    # parses list of database names to remove illegal punction
    # this reduces user confusion
    dbItem = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    dbList.append(dbItem)
    
  print(dbList)
  
  if dbName in dbList:
    print("Error: Database name already in use. DB cannot be created.")
  elif dbName not in dbList:
    addCmd = ("CREATE DATABASE {};")
    mycursor.execute(addCmd.format(dbAdd))
    mydb.commit()
  
def delDB(dbName):

  mycursor.execute("SHOW DATABASES")
  mydb.commit()

  dbList = []
  for x in mycursor:
    filteredx = str(x)
    # parses list of database names to remove illegal punction
    # this reduces user confusion
    dbItem = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    dbList.append(dbItem)
    
  print(dbList)
  
  if dbName not in dbList:
    print("Error: Database does not exist. DB cannot be deleted.")
  elif dbName in dbList:
    dropCmd = ("DROP DATABASE {};")
    mycursor.execute(dropCmd.format(dbDel))
    print("Change committed")
    mydb.commit()

    
  

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
        createTableLoop = True
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
          createTable()
          if createTable() == False:
            tableLoop = True
          else:
            tableLoop = False
          
        elif tableChoice == '3':
          print("Enter the name of the table you would like to delete")
          tableName = input()
          dropTable(dbChosen, tableName)

          tableLoop = True
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
        
        numberC = numCol(dbChosen, dbTableName)
        colNames = colName(dbTableName)
        colNameList = []
        i = 0
        while i < numberC[0]:
          colNameList.insert(i, colNames[i][3])
          i = i + 1
        showFromTable(colNameList, dbTableName)

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
            try:
              print("What is the name of the cell's column?") # 2nd variable tiago
              cellColumn = input()
              print("What is the unique index's column name?") #  4th variable ohm
              cellIndex = input()
              print("What is the unique index number of the cell?") # 5th variable obamna
              cellLocation = input()
              print("What would you like the new cell value to be?") # 3rd variable 12
              cellValue = input()
              update(dbTableName,cellColumn,cellValue,cellIndex,cellLocation)
              updateBool = False
            except:
              print("ERROR: the information you entered in incorrect, please try again")

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
            addRow(dbTableName, numberC[0], colNameList)
            rowBool = False
          
          elif rowModChoice == '2':
            delRow(dbTableName, numberC[0], colNameList)
            rowBool = False

          elif rowModChoice == '3':
            findRow(dbTableName, numberC[0], colNameList)
            rowBool = False
            
          elif rowModChoice == '4':
            rowBool = False

        ######################################################
        # Column manipulation which allows user to add column, remove column, or change column name
        while columnBool:
          
          
          # Getting the user input
          print("Type 1 to add column to table")
          print("Type 2 to remove column from table")
          print("Type 3 to change a column name")
          print("Type 4 to return/exit")
          inputNum = input()
          print("Type the column you would like to manipulate(for removing or changing)/add(new column name, no duplicates)")
          colNum = input()
          
          if input == 4:
            columnBool = False

          ##getting user's input to see which column to add after  
          if inputNum== '1':
            print("Type column name you want to add after")
            afterCol=input()
            columnAdd(dbTableName, colNum, afterCol, colNameList)

          ##getting user's input to see what new column name to change into  
          if inputNum == '3':
            print("Choose new column name to change into: ")
            newCol=input()
            columnChange(dbTableName, colNum, newCol, colNameList)

          ##removing column
          if inputNum=='2':
            columnRemove(dbTableName, colNum, colNameList)
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
        addDB(dbAdd)
        
        userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
        if userEnd=='1':
          dbChoice='0'
        elif userEnd=='2':
          t=False

      elif dbAlter == '2':
          showDataBase()

          print("Please type the name of the database you would like to delete:")
          dbDel = input("Type here: ")
          
          delDB(dbDel)
          
          userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
          if userEnd=='1':
            dbChoice='0'
          elif userEnd=='2':
            t=False
    ## Triggers boolean to exit main program loop if user chooses to exit program   
    while dbChoice == '3':
      t = False


