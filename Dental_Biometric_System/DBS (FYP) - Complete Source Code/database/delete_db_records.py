import mysql.connector
from mysql.connector import Error
import json



# Create connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="forensic_dental_biometrics"
        )
        print("Connection to MySQL database successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred while connecting to the database")
        return None
       
 
 
            
def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed")




    


def check_record_exist(name):
    
    connection = create_connection()
    cursor = connection.cursor()
    try:
        search_query = "SELECT id, name, age, gender, state, picture_address, radiograph_address  FROM Testing1 WHERE name = %s"
        cursor.execute(search_query, (name,))
        result = cursor.fetchone()

        if result:
            record = {
                "id": result[0],
                "name": result[1],
                "age": result[2],
                "gender": result[3],
                "state": result[4],
                "picture_address": result[5],
                "radiograph_address": result[6]
            }
            return record
        else:
            print(f"No record found for the name '{name}'")
            return False

    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return False
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return False
    
    
    
    
def delete_record(name):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        delete_query = "DELETE FROM Testing1 WHERE name = %s"
        cursor.execute(delete_query, (name,))
        connection.commit()
        print(f"All records with name '{name}' deleted successfully")
        return True
    except Error as e:
        print(f"The error '{e}' occurred while deleting records")
        return False





def delete_all_records():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        delete_query = "DELETE FROM Testing1"
        cursor.execute(delete_query)
        connection.commit()
        print("All records deleted successfully")
        return True
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return False
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return False
