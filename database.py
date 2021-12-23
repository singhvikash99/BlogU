#import mysql.Connector
import mysql.connector

#connect to database
conn = mysql.connector.connect(
    user = "root",
    password = "mysql",
    database = "blogu"
)

#creating a cursor object
cusrsor = conn.cursor()

#query for SQL
query = ("select * from users")

#execute SQL query
cusrsor.execute(query)

#kept result in a variable res
res = cusrsor.fetchall()

#printing data fetched from database
print (res)

#closing connection 
conn.close()