import mysql.connector
from db_config import connect_to_db
from PIL import Image
from io import BytesIO
import cv2 as cv
from datetime import datetime  # Import datetime

# Function to insert patient record into the database
def insert_patient(name, age, gender, diagnosis, image_blob):
    try:
        # Connect to the database
        connection = connect_to_db()
        
        if connection:
            print("Database connection established successfully.")
        else:
            print("Failed to connect to the database.")
            return
        
        cursor = connection.cursor()
        
        # SQL query to insert data
        query = """
        INSERT INTO patients (name, age, gender, diagnosis, image_path,created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        current_timestamp = datetime.now()
        # Execute the query, image_blob will be None (NULL in SQL)
        cursor.execute(query, (name, age, gender, diagnosis, image_blob,current_timestamp))
        
        # Commit the transaction
        connection.commit()
        
        print("Patient record inserted successfully!")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the connection
        if connection:
            connection.close()
            print("Database connection closed.")



