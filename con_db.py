import MySQLdb as connector
mydb = connector.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1234'
)
my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS users")
my_cursor.execute("SHOW DATABASES")
my_cursor.execute("use users")
my_cursor.execute('Create table IF NOT EXISTS user_table(email varchar(200) primary key,password varchar(200),name varchar(200),address varchar(1000),city varchar(200),pincode varchar(12))')
# for db in my_cursor:
#     print(db)
# for data in my_cursor:
#     print(data)