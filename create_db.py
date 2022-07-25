import mysql.connector

my = mysql.connector.connect(
host= "localhost",
user = "alihydir",
passwd  = "helloali",
)

my_cursor = mydb.cursor()
my_cursor.execute("create database users")

my_cursor.execute("show database")

for db in my_cursor:
    print(db)
