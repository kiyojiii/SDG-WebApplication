import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = ''
)

# # prepare a cursor object
# cursorObject = dataBase.cursor()

# # create a database
# cursorObject.execute("CREATE DATABASE vehisense")

# print("Success")