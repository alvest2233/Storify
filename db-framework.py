#from 3b1wDBclasses import * 
import mysql.connector
#from functions import *
from prettytable import PrettyTable

# uses MYSQL connector to establish framework connection to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="password"
)

########################################################################### LEARN WHAT THIS MEANS
mycursor = mydb.cursor(buffered=True)
t = True

# Function to show the database
def showDataBase():
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    filteredx = str(x)
    # parses list of database names to remove illegal punctuation
    # this reduces user confusion
    a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    print(a)
    print("")

def columnAdd(tableName, newCol, colNameList):
    # Add a new column with a name of their choice
    
    # inner loop keeps function cycling through column name list
    innerLoop = True

    #outer loop 
    outerLoop = True
    while outerLoop:
      for x in colNameList:
        if x == newCol:
          innerLoop = False
      if innerLoop == False:
        print("The name you entered already exists. Please choose a new column name to add:")
        newCol = input()
        innerLoop = True
      else:
        outerLoop = False
    
    addC = "ALTER TABLE {} ADD {} VARCHAR(255)"
    mycursor.execute(addC.format(tableName, newCol))
    print("\n")
    mydb.commit()
      
    
def columnChange(tableName, colNameList):
    print("Please enter the old column name:")
    oldCol = input()
    innerRedo = True
    redo = True
    while redo:
      for x in colNameList:
        if x != oldCol:
          innerRedo = True
        else:
          innerRedo = False
          break
      if innerRedo == True:
        print("The name you entered does not exist. Please choose a column name to change:")
        oldCol = input()
        redo = True
      else:
        redo = False
    
        

    print("Choose new column name to change into:")
    newCol = input()
    innerRedo2 = True
    redo2 = True
    while redo2:
      for x in colNameList:
        if x != newCol:
          innerRedo2 = False
        else:
          innerRedo2 = True
          break
      if innerRedo2 == True:
        print("The name you entered does not exist. Please choose a column name to change:")
        newCol = input()
        redo2 = True
      else:
        redo2 = False
    
        
    modC = "ALTER TABLE `{}` RENAME COLUMN {} TO {}"
    mycursor.execute(modC.format(tableName, oldCol, newCol))
    print("\n")
    mydb.commit()

def columnRemove(tableName, columnName, colNameList):
    # Drop the column based on its name 
    innerLoop = True
    outerLoop = True
    while outerLoop:
      for x in colNameList:
        if x == columnName:
          innerLoop = True
        else:
          innerLoop = False 
      if innerLoop == False:
        print("The name you entered does not exist. Please choose a new column name to remove: ")
        columnName = input()
        innerLoop = True
      else:
        outerLoop = False

    dropC = "ALTER TABLE {} DROP COLUMN {}"
    mycursor.execute(dropC.format(tableName, columnName))
    print("\n")
    mydb.commit()

def numCol(DBName, tableName):
    #creates string with SQL command to grab all columns from table via SQL, using requested database and table
    numC = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = '{}' AND table_name = '{}'"
    
    #executes string command with database name and table name values obtained from method call
    mycursor.execute(numC.format(DBName, tableName))
    col = mycursor.fetchall()
    mydb.commit()
    
    #for loop increases for each column name
    for x in col:
      return x

def colName(tableName):
    #creates string containing SQL command to grab all columns from table via SQL in order by which they were obtained
    cName = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS where table_name = '{}' order by ORDINAL_POSITION"
    
    #executes command, gets column in list format and returns it
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
    print("\n")
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
      
      if innerTest == True:
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
    
def update(tableName, colNames):
  
  print("What is the name of the cell's column?") # 2nd variable tiago
  cellColumn = input()
  innerLoop = True
  outerLoop = True
  while outerLoop:
    for x in colNames:
      if x == cellColumn:
        innerLoop = True
        break
      else:
        innerLoop = False 
    if innerLoop == False:
      print("The name you entered does not exist. Please choose a column that exists: ")
      cellColumn = input()
      innerLoop = True
    else:
      outerLoop = False
  
  print("What is the unique index's column name?") #  4th variable ohm
  cellIndex = input()
  innerLoop2 = True
  outerLoop2 = True
  while outerLoop2:
    for x in colNames:
      if x == cellIndex:
        innerLoop2 = True
        break
      else:
        innerLoop2 = False 
    if innerLoop2 == False:
      print("The name you entered does not exist. Please choose a column that exists: ")
      cellIndex = input()
      innerLoop2 = True
    else:
      outerLoop2 = False

  print("What is the unique index number of the cell?") # 5th variable obamna
  cellLocation = input()
  columnInfo = "SELECT {} FROM {}"
  mycursor.execute(columnInfo.format(cellIndex, tableName))
  results = mycursor.fetchall()
  mydb.commit()
  tableList = []
  for x in results:
    results = str(x)
    a = results.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    tableList.append(a)
  
  innerLoop3 = True
  outerLoop3 = True
  while outerLoop3:
    for x in tableList:
      if x == cellLocation:
        innerLoop3 = True
        break
      else:
        innerLoop3 = False 
    if innerLoop3 == False:
      print("The value you entered does not exist. Please choose a value that exists: ")
      cellLocation = input()
      innerLoop3 = True
    else:
      outerLoop3 = False

  print("What would you like the new cell value to be?") # 3rd variable 12
  cellValue = input()
  # Takes table name, desired set value, the value it will be changed to, the condition for the change and what the condition will apply to 
  try:
    sql = "UPDATE {} SET {} = '{}' WHERE {} = '{}'"
  
  # Take the given parameters and input them into the right position
  
    mycursor.execute(sql.format(tableName, cellColumn, cellValue, cellIndex, cellLocation))
    mydb.commit()
  except:
    print("Input for tableName/columnName/whereCondition do not exist in database")  
  print("\n")  
    
def showAllDBTables(dbName):
  # checks database if tables exist, prints error message instead of DB table if no tables exist in DB
  tables = "SHOW TABLES IN {}"
  try:
    #if tables exist, it executes the command, grabs tables, filters the text and outputs all existing tables for the user
     mycursor.execute(tables.format(dbName))
     mydb.commit()
     prompt = "\nTables in {}"
     print(prompt.format(dbName))
     for x in mycursor:
      filteredx = str(x)
      a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
      print(a)
  except:
    #if tables do not exist, error message displays. elsewhere in code, user will be returned to the previous loop
    print("\nTable preview unavailable, no tables currently exist in the DB")
  
def showFromTable(columnNameList, tableName):
  
  #
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
      
  except:
      print("There are no valid databases. Please create a DB first")
      
  while True:
    print("Input the name of the table. Please use a unique name")
    newTN = input()
    # newTN = newTN.lower()

    if newTN not in tableList:
      
      while True:
        try:
          print("Enter the number of columns you would like to have")
          numColumns = int(input())
          if(numColumns > 0):
            break
          else:
            print("ERROR: The number you have added is invalid number value")
        except:
          print("ERROR: The number you have added is invalid number value")
          
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
          createTableScript += ("`" + colNames[i] + "` VARCHAR(255))")
        else:
          createTableScript += ("`" + colNames[i] + "` VARCHAR(255), ")  
       
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
      
      print("\n")

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
    
  
  
  if dbName in dbList:
    print(dbList)
    print("Error: Database name already in use. DB cannot be created.")
  elif dbName not in dbList:
    addCmd = ("CREATE DATABASE {};")
    mycursor.execute(addCmd.format(dbAdd))
    mydb.commit()
    print("New database added")
  
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
    
    
  if dbName not in dbList:
    print(dbList)
    print("ERROR: Database does not exist. DB could not be deleted.")
  elif dbName in dbList:
    dropCmd = ("DROP DATABASE {};")
    mycursor.execute(dropCmd.format(dbDel))
    print("Change committed")
    mydb.commit()
    print("Database has been removed")
    
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
      
      try:
        dbChosen = input("Selected database: ")
        
        useDB = "USE {}"
        mycursor.execute(useDB.format(dbChosen))
      except:
        print("ERROR: The database you entered does not exist, please enter a database that exists\n")
        break

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
          showAllDBTables(dbChosen)
          createTable()
          tableLoop = False
          
        elif tableChoice == '3':
          showAllDBTables(dbChosen)
          print("Enter the name of the table you would like to delete")
          tableName = input()
          dropTable(dbChosen, tableName)

          tableLoop = True
        elif tableChoice == '4':  
            break 
            
      if tableChoice == '4':
        break

      # prompts user for desired table, sends to table modification loop
      showAllDBTables(dbChosen)
      print("Please state the table you would like to access:")
      
      validTables = "SHOW TABLES IN {}"
      mycursor.execute(validTables.format(dbChosen))
      results = mycursor.fetchall()
      mydb.commit()

      tableList = []
      for x in results:
        results = str(x)
        a = results.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        tableList.append(a)
        
      dbTableName = input("Type table name: ")
      notFound = False
      for x in tableList:
        if x == dbTableName:
          notFound = False
          break
        else:
          notFound = True
      
      if notFound:
        tableModLoop = False
        print("The table does not exist")
      else:
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
          update(dbTableName, colNameList)
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
          
          if inputNum == 4:
            columnBool = False

          ##getting user's input to see which column to add after  
          elif inputNum == '1':
            print("Type column name you want to add")
            addCol = input()
            columnAdd(dbTableName, addCol, colNameList)

          ##getting user's input to see what new column name to change into  
          elif inputNum == '3':
            columnChange(dbTableName, colNameList)

          ##removing column
          elif inputNum =='2':
            print("Please enter the column name you want to remove: ")
            removeCol = input()
            columnRemove(dbTableName, removeCol, colNameList)
          columnBool = False
        ######################################################
        # Return to main selection screen
        if dbModChoice == '4':
          tableModLoop = False
 
    ##if user picks 2, ask if user wants to create or delete a database, get user input
    while dbChoice == '2':
      print("Type 1 to create a database")
      print("Type 2 to delete a database")
      print("Type 3 to return to main menu")
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
          exit()

      elif dbAlter == '2':
          showDataBase()

          print("Please type the name of the database you would like to delete:")
          dbDel = input("Type here: ")
          
          delDB(dbDel)
          
          userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
          if userEnd=='1':
            dbChoice='0'
          elif userEnd=='2':
            exit()

      elif dbAlter == '3':
        dbChoice='0'
    ## Triggers boolean to exit main program loop if user chooses to exit program   
    while dbChoice == '3':
      exit()


