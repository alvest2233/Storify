import mysql.connector
from prettytable import PrettyTable

# uses MYSQL connector to establish framework connection to MySQL database
mydb = mysql.connector.connect(
  # your network name, DB username and DB password here
  host="***********",
  user="***********",
  password="***********"
)

# Creates cursor to fetch data from the database server
# This links the framework to the database server and allows for the execution of commands
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



# Add a new column with a name of their choice
def columnAdd(tableName, newCol, colNameList):
    # The inner loop checks if the name exists already and then the outer loop reprompts the user if the name already exists
    innerLoop = True 
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
    
    # Changing the table to add the new column and committing the change
    addC = "ALTER TABLE `{}` ADD {} VARCHAR(255)"
    mycursor.execute(addC.format(tableName, newCol))
    print("\n")
    mydb.commit()



# Changing a column name to another name
def columnChange(tableName, colNameList):
    # Prompting the user to input the name of the column they want to change
    print("Please enter the old column name:")
    oldCol = input()
    
    # The inner loop checks if the name exists already and then the outer loop reprompts the user if the name does not already exists
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
    
        
    # The inner loop checks if the name exists already and then the outer loop reprompts the user if the name already exists
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
    
    # Changing the table to change the column name and committing the change
    # Backticks are to bulletproof user inputs in case a restricted word or character is a table or column name
    modC = "ALTER TABLE `{}` RENAME COLUMN `{}` TO `{}`"
    mycursor.execute(modC.format(tableName, oldCol, newCol))
    print("\n")
    mydb.commit()



# Drop the column based on its name 
def columnRemove(tableName, columnName, colNameList):
    # The inner loop checks if the name exists already and then the outer loop reprompts the user if the name does not already exists
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

    # Changing the table to delete the column and committing the change
    dropC = "ALTER TABLE `{}` DROP COLUMN `{}`"
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



# Add a row to the table
def addRow(tableName, numCol, colNames):
    # Reformat the column names list so the ticks and comma's can be removed
    columns = "("
    between = ", "
    i = 0
    while i < numCol:
      columns = "".join([columns, colNames[i]])
      columns = "".join([columns, between])
      i = i + 1
    columns = columns[:-2]
    columns = "".join([columns, ")"])

    # Prompting user to input values for each column with the column name
    i = 0
    inputs = []
    prompt = "Please input the value for the column "
    
    # Concatenation so only the column name is printed and nothing else
    while i < numCol:
        tempVar = "".join([prompt, colNames[i]])
        print("".join([tempVar, ":"]))
        answer = input()
        inputs.insert(i, answer)
        i = i + 1
    x = str(inputs)
    x = x.replace("[", "(").replace("]", ")")
    
    # Adding the row into the table and then committing the change
    test = ("INSERT INTO `{}` {} VALUES {}")
    columns = columns.replace("(", "(`").replace(")", "`)")
    print(columns)
    mycursor.execute(test.format(tableName, columns, x))
    print("\n")
    mydb.commit()



# Delete a row from the table
def delRow(tableName, numCol, colNames):
    test = False
    innerTest = False
    
    # Loop to keep running the entire code repeatedly
    while test == False:
      try:
        # Prompt for user input of column name to isolate the row which needs to be deleted
        prompt = "Please enter the name of the unique index column: "
        columns = "("
        between = ", "
        i = 0
        
        # Reformat the column names list so the ticks and comma's can be removed
        while i < numCol:
          columns = "".join([columns, colNames[i]])
          columns = "".join([columns, between])
          i = i + 1
        columns = columns[:-2]
        columns = "".join([columns, ")"])
        print("".join([prompt, columns]))
        columnName = input()
        
        # Prompting the user to input a unique index to isolate the row
        print("Please enter the unique index of the row you would like to delete: ")   
        value = input()
        
        # Finding the all the row values for the column that was input
        existCheck = "SELECT `{}` FROM `{}`"
        mycursor.execute(existCheck.format(columnName, tableName))
        myresult = mycursor.fetchall()
        tableList = []
        
        # Getting all the row index's from the column 
        for x in myresult:
          myresult = str(x)
          a = myresult.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
          tableList.append(a)
        
        # If the row index is in the list above then excute the code to remove the row
        for x in tableList:
          if value == x:
            innerTest = True
        
        # Code to remove the row if it is found and then breaking out of the loop
        if innerTest:
          dRow = "DELETE FROM `{}` WHERE `{}` = '{}'"
          mycursor.execute(dRow.format(tableName, columnName, value))
          mydb.commit()
          print("Row has been removed")
          test = True
        
        # Prompting user to input another value
        else:
          innerTest = False
          print("The row does not exist. Please try again and make sure the correct information is entered.")
        
      # Prompting user ot input another value if there are any errors
      except:
        print("The row does not exist. Please try again and make sure the correct information is entered.")



# Finding and returning a row
def findRow(tableName, numCol, colNames):
    test = False
    innerTest = False
    
    # Loop to keep running the entire code repeatedly
    while test == False:
      try:
        # Prompt for user input of column name to isolate the row which needs to be found
        prompt = "Please enter the name of the unique index column: "
        columns = "("
        between = ", "
        i = 0
        
        # Reformat the column names list so the ticks and comma's can be removed
        while i < numCol:
          columns = "".join([columns, colNames[i]])
          columns = "".join([columns, between])
          i = i + 1
        columns = columns[:-2]
        columns = "".join([columns, ")"])
        print("".join([prompt, columns]))
        columnName = input()

        # Prompting the user to input a unique index to isolate the row
        print("Please enter the unique index of the row you would like to find: ")   
        value = input()

        # Finding the all the row values for the column that was input
        existCheck = "SELECT `{}` FROM `{}`"
        mycursor.execute(existCheck.format(columnName, tableName))
        myresult = mycursor.fetchall()
        mydb.commit()

        # Getting all the row index's from the column
        tableList = []
        for x in myresult:
          myresult = str(x)
          a = myresult.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
          tableList.append(a)
        
        # If the row index is in the list above then excute the code to find the row
        for x in tableList:
          if value == x:
            innerTest = True
        
        # Code to remove the row if it is found and then breaking out of the loop
        if innerTest:
          fRow = "SELECT * FROM `{}` WHERE `{}` = '{}'"
          mycursor.execute(fRow.format(tableName, columnName, value))
          result = mycursor.fetchall()
          mydb.commit()
          test = True
          
        # Prompting user to input another value 
        else:
          innerTest = False
          print("The row does not exist. Please try again and make sure the correct information is entered.")
          
      # Prompting user ot input another value if there are any errors
      except:
        print("The row does not exist. Please try again and make sure the correct information is entered.")
      
      if innerTest == True:
        searchResults = "\nResults found for `{}` = '{}':"
        print(searchResults.format(columnName, value)) 

        #declares PrettyTable, and sets its columns equal to the given column names
        displayDB = PrettyTable()
        displayDB.field_names = colNames
        
        #attempts to fetch all rows from the result list fetched by the cursor
        #If rows are returned, it adds them line by line thanks to the for _ in _ loop
        #if no rows are returned, prints error message
        try:
          for x in result:
            displayDB.add_row(x)  
          print(displayDB)
          print ("\n")
        except:
          print("ERROR: TABLE COULD NOT PRINT PLEASE TRY AGAIN LATER")
    

# Changes single cell in table given the names of a table and its columns    
def update(tableName, colNames):
  
  print("What is the name of the cell's column?")
  
  # The inner loop checks if the name exists already and then the outer loop reprompts the user if the name does not exist
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
    #if user inputed column name doesn't exist in list of columns, prompt user to input another column name
    if innerLoop == False:
      print("The name you entered does not exist. Please choose a column that exists: ")
      cellColumn = input()
      innerLoop = True
    else:
      outerLoop = False
  
  # The inner loop checks if the name exists already and then the outer loop reprompts the user if the name does not exist
  print("What is the unique index's column name?")
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
    #if user inputed column name doesn't exist in list of columns, prompt user to input another column name
    if innerLoop2 == False:
      print("The name you entered does not exist. Please choose a column that exists: ")
      cellIndex = input()
      innerLoop2 = True
    else:
      outerLoop2 = False

  # Prompts user to enter a value to isolate a row then a cell
  print("What is the unique index number of the cell?") 
  cellLocation = input()
  columnInfo = "SELECT `{}` FROM `{}`"
  mycursor.execute(columnInfo.format(cellIndex, tableName))
  results = mycursor.fetchall()
  mydb.commit()
  tableList = []

  # filtering tablelist to remove certain special characters from fetched cursor output
  for x in results:
    results = str(x)
    a = results.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    tableList.append(a)
  
  # The inner loop checks if the name exists already and then the outer loop reprompts the user if the name does not exist
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

  print("What would you like the new cell value to be?")
  cellValue = input()
  # Takes table name, desired set value, the value it will be changed to, the condition for the change and what the condition will apply to 
  try:
    sql = "UPDATE `{}` SET `{}` = '{}' WHERE `{}` = '{}'"
  
  # Take the given parameters and input them into the right position
  
    mycursor.execute(sql.format(tableName, cellColumn, cellValue, cellIndex, cellLocation))
    mydb.commit()
  except:
    print("Input for tableName/columnName/whereCondition do not exist in database")  
  print("\n")  



#function to show all tables within the database passed through the parameter    
def showAllDBTables(dbName):
  #checks database if tables exist, prints error message instead of DB table if no tables exist in DB
  tables = "SHOW TABLES IN `{}`"
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
  

  
#Function to read all elements in a table, and use the PrettyTable library to display it visually using ASCII art  
def showFromTable(columnNameList, tableName):
  
  #declares new table and makes its columns equal to the column list created 
  displayDB = PrettyTable()
  displayDB.field_names = columnNameList

  #attempts to grab all column info from tables if accessible
  try:
    #cursor fetches all column data from table and adds it to the 'results' list
    table = "SELECT * FROM `{}`"
    mycursor.execute(table.format(tableName))  
    results = mycursor.fetchall()
    mydb.commit()

    #if successful, each row of values in the list 'results' is added to the table
    for x in results:
      displayDB.add_row(x)  
    
    # outputs the table
    print(displayDB)
    print ("\n")
    
  #if the table info is inaccessible, it outputs an error message
  except:
    print("ERROR: TABLE COULD NOT PRINT PLEASE TRY AGAIN LATER")



#function to check if a table name is valid, specifically that it is not in use by another table in the database (DB)
def createTable():
  #String prompt to get a list of all tables in any given DB
  validTables = "SHOW TABLES IN `{}`"
  try:
      #executes string prompt with global database variable from when an existing database was chosen in the first loop
      mycursor.execute(validTables.format(dbChosen))
      mydb.commit()

      #initializes a list and fills it with the data fetched from the command
      tableList = []
      for x in mycursor:
        #in a loop, all data fetched from SHOW TABLES is stripped of unnecessary punctuation, so that it can be compared with user input
        filteredx = str(x)
        a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        #the table names are added to the list once they are filtered properly
        tableList.append(a)
  #if the program is unable to locate the tables in a DB, it outputs this error message and exits the method    
  except:
      print("There are no valid databases. Please create a DB first")
  
  #outer loop continuously prompts user for a table input until a valid table name is inputted
  while True:
    print("Input the name of the table. Please use a unique name")
    newTN = input()

    #accesses inner loop if table name is valid (not in the fetched list of table names in DB)
    if newTN not in tableList:
      
      while True:
        # prompts user for number of columns, sends error message if non integers or numbers less than 1 are inputted, loop prompts user for new input
        try:
          print("Enter the number of columns you would like to have")
          numColumns = int(input())
          if(numColumns > 0):
            break
          else:
            print("ERROR: The number you have added is invalid number value")
        except:
          print("ERROR: The number you have added is invalid number value")

      #once loop exited, number of columns input is casted to integer and a MySQL script to create a table with the desired column    
      numColumns = (int)(numColumns)
      colNames = []
      createTableScript = "CREATE TABLE `{}` ("
      
      #prompts user for a column name for each 
      for i in range(numColumns):
        colPrompt = "Enter name for column {}"
        index = i + 1
        print(colPrompt.format(index))
        temp = input()
        
        #makes user choose unused column name if duplicate name is chosen
        while temp in colNames:
          print("Error: column name already in use")
          colPrompt = "Enter a new name for column {}"
          print(colPrompt.format(index))
          temp = input()
        
        #adds column names to list, and formats the text so that restricted words and characters won't 
        #break their input, and so that their column can store up to 255 characters per cell (the program's standard)
        colNames.append(temp)
        if i == (numColumns - 1):
          createTableScript += ("`" + colNames[i] + "` VARCHAR(255))")
        else:
          createTableScript += ("`" + colNames[i] + "` VARCHAR(255), ")  
       
       #If table construction does not work, prints error message and exits loop
      try:
        mycursor.execute(createTableScript.format(newTN))
        mydb.commit()
      except:
        print("ERROR: TABLE UNABLE TO BE CREATED")
      break 

    #if the table name already exists in the list, prints error message and prompts user for new name thanks to loop    
    elif newTN in tableList:
      print("Table name already in use, and cannot be created")



#Function to delete a table based on the database it is located in and the table name
def dropTable(dbChosen, tableName):
  #variable to show to tables located in the database passed through the parameters
    validTables = "SHOW TABLES IN `{}`"
    
    
    try:
      #pass the database from the parameter into validTables variable
      mycursor.execute(validTables.format(dbChosen))
      mydb.commit()

      #filter the table names to remove certain special characters
      tableList = []
      for x in mycursor:
        filteredx = str(x)
        a = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        tableList.append(a)
      
      print("\n")

      #if the table name given through the parameters exists in the table list, remove it
      if tableName in tableList:
        deleteTableScript = "DROP TABLE `{}`"
        mycursor.execute(deleteTableScript.format(tableName))
        mydb.commit()
        print("Table {} has been dropped".format(tableName))
      #if the table name given throguh the parameters doesn't exist in the table list, print an error message
      else:
        print("Table does not exist, and cannot be deleted.")  
    #If no databases are found, throw an exception to catch the error 
    except:
      print("There are no valid databases. Please create a DB first")



#adds database to server if its name is not currently in use
def addDB(dbName):

#calls command to display databases, commits change 
  mycursor.execute("SHOW DATABASES")
  mydb.commit()

  dbList = []
  for x in mycursor:
    filteredx = str(x)
    # parses list of database names to remove illegal punction
    # this reduces user confusion
    dbItem = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    dbList.append(dbItem)
    
  
  ##checks for name use in server, if it is already usedm it prints an error, otherwise it calls the command
  if dbName in dbList:
    print(dbList)
    print("Error: Database name already in use. DB cannot be created.")
  elif dbName not in dbList:
    addCmd = ("CREATE DATABASE `{}`;")
    mycursor.execute(addCmd.format(dbAdd))
    mydb.commit()
    print("New database added")
  


#deletes database from server if database requested exists
def delDB(dbName):

  #calls command to display databases, commits change 
  mycursor.execute("SHOW DATABASES")
  mydb.commit()

  dbList = []
  for x in mycursor:
    filteredx = str(x)
    # parses list of database names to remove illegal punction
    # this reduces user confusion
    dbItem = filteredx.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
    dbList.append(dbItem)
    
  ##checks for name use in server, if it is not already used, it prints an error, otherwise it calls the command
  if dbName not in dbList:
    print(dbList)
    print("ERROR: Database does not exist. DB could not be deleted.")
  elif dbName in dbList:
    dropCmd = ("DROP DATABASE `{}`;")
    mycursor.execute(dropCmd.format(dbDel))
    print("Change committed")
    mydb.commit()
    print("Database has been removed")
    

################################################### Functions above, main method below ###################################################


print("Welcome to Storify!")
# loop used to ensure that the user can use the program over again until they want to exit
while t:
    #let user know what they would like to do, access database, create/delete database, or exit
    print("Type 1 if you have an existing database you would like to access")
    print("Type 2 if you would like to create or delete a database")
    print("Type 3 to exit the program")
    #user input
    
    #loop to validate user input
    while True:
      dbChoice = input("Type here: ")
      
      #if user input is valid, break out of the loop
      if dbChoice == '1' or dbChoice == '2' or dbChoice == '3':
        break
      #if user input doesn't match the choices they are given, print an error message and let user type another input
      else:
        print("The input entered in incorrect, please type in the right value")


    # checking input from user to see if they want to create/delete a database or open an existing one
    while dbChoice == '1':
      print("You choose that you would like to open an existing database please wait...")
      
      #prompts user for DB holding desired table, shows tables in DB
      showDataBase()
      print("Please list the database your table is located in:")
      
      #take the user input and check if it is in the list of databases, if it is, use it for further code
      try:
        dbChosen = input("Selected database: ")
        
        useDB = "USE `{}`"
        mycursor.execute(useDB.format(dbChosen))
      #if user provided database doesn't exist, print error message and send user back to to the start
      except:
        print("ERROR: The database you entered does not exist, please enter a database that exists\n")
        break

      # OPTIONS FOR ACCESSING / CREATING TABLE
      
      tableLoop = True
      while tableLoop == True:
        #ask user what they would like to do after selecting a database, access table, 
        createTableLoop = True
        print("Type 1 if you have an existing table you would like to access")
        print("Type 2 if you would like to create a table")
        print("Type 3 if you would like to delete a table")
        print("Type 4 if you would like to return")
        tableChoice = input()
        
        #if user input is 1, send user to accessing an existing table by kicking them out of the current loop
        if tableChoice == '1':
          tableLoop = False

        #if user input is 2, create table using the createTable function and then kick them out of the current loop
        elif tableChoice == '2':
          showAllDBTables(dbChosen)
          createTable()
          tableLoop = False
        
        #if user input is 3, prompt user for the name of table they would like to delete and use dropTable function to delete the table
        elif tableChoice == '3':
          showAllDBTables(dbChosen)
          print("Enter the name of the table you would like to delete")
          tableName = input()
          dropTable(dbChosen, tableName)
          tableLoop = True

        #if user chooses 4, exit table loop
        elif tableChoice == '4':  
            break 
      #if user chooses 4, exit dbchoice loop      
      if tableChoice == '4':
        break

      #prompts user for desired table, sends to table modification loop
      showAllDBTables(dbChosen)
      print("Please state the table you would like to access:")
      
      #getting tables from selected database
      validTables = "SHOW TABLES IN `{}`"
      mycursor.execute(validTables.format(dbChosen))
      results = mycursor.fetchall()
      mydb.commit()

      #filters table list to remove certain special characters
      tableList = []
      for x in results:
        results = str(x)
        a = results.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        tableList.append(a)
      
      #getting table name input from user to use for table modifications 
      #if user inputs an invalid name, display a not found message and do not send user to the table mod loop
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

      #table modification loop, shows current table, prompts user for change then breaks off into chosen options
      while tableModLoop: 
        
        #getting number of columns and column names, then display the table to the user
        numberC = numCol(dbChosen, dbTableName)
        colNames = colName(dbTableName)
        colNameList = []
        i = 0
        while i < numberC[0]:
          colNameList.insert(i, colNames[i][3])
          i = i + 1
        showFromTable(colNameList, dbTableName)

        #booleans to help with looping different modifications options
        updateBool = False
        rowBool = False
        columnBool = False
        
        #display table mod options to prompt the user for a response and collect the user's input to send them to the mod loop option they picke
        print("Type 1 to change a single cell")
        print("Type 2 to change a row")
        print("Type 3 to change a column")
        print("Type 4 to exit the program or return to the previous options")
        dbModChoice = input()
        
        #loop to check if user's input is a valid option, set the boolean variables to their respective T/F and break loop
        while True: 
          if dbModChoice == '1':
            updateBool = True
            break
          elif dbModChoice == '2':
            rowBool = True
            break
          elif dbModChoice == '3':
            columnBool = True
            break
          elif dbModChoice == '4':
            tableModLoop = False
            dbChoice = '0'
            break
           #if user input doesn't match any of the given options, print an error message and allow user to give another value
          else:
            print("Invalid option, please input 1 for updating a single cell, 2 to modify a row, 3 to modify a column, or 4 to exit program")
            dbModChoice=input("Enter valid option here: ")
        #################################################################################
        
        #single cell replacement user prompts, inputs sent to single cell update method
          
        while updateBool:
          update(dbTableName, colNameList)
          updateBool = False

        ######################################################

        #Row manipulation, prompts user for adding row, removing row, or finding a desired row
        while rowBool:
          print("Type 1 to add a row from the table")
          print("Type 2 to remove a row from the table")
          print("Type 3 to find your desired row")
          print("Type 4 to return/exit")
          rowModChoice = input()
        
          #Ask user for the values they would like to add to the new row and display the new row after
          if rowModChoice == '1':          
            addRow(dbTableName, numberC[0], colNameList)
            rowBool = False
          #Ask user for the row that they would like to remove from the table
          elif rowModChoice == '2':
            delRow(dbTableName, numberC[0], colNameList)
            rowBool = False
          #Ask user for what row they would like to find on the table
          elif rowModChoice == '3':
            findRow(dbTableName, numberC[0], colNameList)
            rowBool = False
          #exits row modify loop  
          elif rowModChoice == '4':
            rowBool = False

        ######################################################
        #Column manipulation which allows user to add column, remove column, or change column name
        while columnBool:
          
          # Getting the user input
          print("Type 1 to add column to table")
          print("Type 2 to remove column from table")
          print("Type 3 to change a column name")
          print("Type 4 to return/exit")
          inputNum = input()
          
          #exits column modify loop if user inputs 4
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
        #return to main selection screen
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
        
        # asking if the user wants to continue or not with the program, then use the input from user to end or continue the loop
        userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
        while True:
          if userEnd=='1':
            dbChoice='0'
            break
          elif userEnd=='2':
            exit()
          else:
            userEnd=input("Invalid option, please re-enter here: ")  
      
      #if user picked 2, delete database (probably should add bullet proofing)
      elif dbAlter == '2':
          #display list of databases to user
          showDataBase()
          
          #getting user input on what database to delete
          print("Please type the name of the database you would like to delete:")
          dbDel = input("Type here: ")
          
          #deleting database that user selected
          delDB(dbDel)
          
          #asking if the user wants to continue or not with the program, then use the input from user to end or continue the loop
          userEnd=input("Do you want to continue or end program(1 to continue or 2 to end): ")
          while True:
            if userEnd=='1':
              dbChoice='0'
              break
            elif userEnd=='2':
              exit()
            else:
              userEnd=input("Invalid option, please re-enter here: ")
      #exit loop
      elif dbAlter == '3':
        dbChoice='0'
    ##triggers boolean to exit main program loop if user chooses to exit program   
    while dbChoice == '3':
      exit()