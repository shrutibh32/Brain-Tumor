import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="soumyabh@123",
        database="brain_tumor_db"
    )
