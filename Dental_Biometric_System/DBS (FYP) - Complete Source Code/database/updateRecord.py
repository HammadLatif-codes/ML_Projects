import mysql.connector
from mysql.connector import Error
import json

def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'forensic_dental_biometrics'")
            database_exists = cursor.fetchone()

            if not database_exists:
                cursor.execute("CREATE DATABASE forensic_dental_biometrics")
                print("Database created successfully")
            else:
                print("Database already exists")

    except Error as e:
        print(f"Error creating database: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")


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

# update recor
def update_record(connection, cursor, record_id, updated_data):
    try:
        update_query = """
            UPDATE Testing1 
            SET name = %s, 
                age = %s, 
                gender = %s, 
                state = %s, 
                picture_address = %s, 
                radiograph_address = %s, 
                decimal_list = %s
            WHERE id = %s
        """
        update_values = (
            updated_data["name"],
            updated_data["age"],
            updated_data["gender"],
            updated_data["state"],
            updated_data["picture_address"],
            updated_data["radiograph_address"],
            json.dumps(updated_data["dental_features"]),
            record_id
        )
        cursor.execute(update_query, update_values)
        connection.commit()
        print(f"Record with ID {record_id} updated successfully")
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
    except Exception as ex:
        print(f"Other Error: {str(ex)}")




def db_operations(id, details_instance,  extracted_features):
    name = details_instance.username
    age = details_instance.age
    gender = details_instance.gender
    state = details_instance.state
    picture_file_path = details_instance.picture_file_path
    radiograph_file_path = details_instance.radiograph_file_path

    connection = create_connection()
    cursor = connection.cursor()

    data = {
            "name": name,
            "age": age,
            "gender": gender,
            "state": state,
            "picture_address": picture_file_path,
            "radiograph_address": radiograph_file_path,
            "dental_features": extracted_features
        }

    update_record(connection, cursor, id ,data)
    close_connection(connection, cursor)