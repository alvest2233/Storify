import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="3b1w",
  password="password"
)
mycursor = mydb.cursor(buffered=True)

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

def addRow(tableName, numCol, colNames):
    # UNTESTED CODE
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

def delRow(tableName, columnName, value):
    dRow = "DELETE FROM {} WHERE {} = '{}'"
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
  
def showFromTable(columnNameList, tableName):
  displayDB = PrettyTable()
  
  displayDB.field_names = columnNameList
  print("colNameList added!\n")

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
      

  print("Input the name of the table. Please use a unique name")
  newTN = input()

  while newTN not in tableList:
    print("Enter the number of columns you would like to have")
    numColumns = input()
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
      break
    except:
      print("ERROR: TABLE UNABLE TO BE CREATED")
      break
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
