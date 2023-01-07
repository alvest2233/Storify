class Functions:
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