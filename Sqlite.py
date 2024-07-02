import sqlite3
from sqlite3 import Error
#Hàm này tạo một kết nối đến cơ sở dữ liệu SQLite
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
connection = create_connection("sm_app.sqlite")
#Hàm này thực hiện một truy vấn SQL trên DB được kết nối và cam kết (commit) các thay đổi.
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
#Hàm thực hiện đọc câu hỏi GoHistory trong DB
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
create_users_table = """

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  tag TEXT NOT NULL
);
"""
execute_query(connection,create_users_table)
create_users = """INSERT INTO users (question,tag) VALUES (?,'diemchuan'),"""
#Hàm thực hiện thêm câu hỏi GoHistory trong DB
def execute_query_insert(connection,question,tag):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute("INSERT INTO users (question,tag) VALUES (?,?)", (question,tag))
        connection.commit()
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
#Hàm thực hiện xóa câu hỏi GoHistory trong DB
def execute_query_delete(connection,id):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute("DELETE FROM users where id=?",(id,))
        connection.commit()
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

