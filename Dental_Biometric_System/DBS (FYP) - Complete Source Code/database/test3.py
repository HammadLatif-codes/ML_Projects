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



# create table for Records
def create_table(connection, cursor):
    try:

        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS Testing1(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                gender VARCHAR(10),
                state VARCHAR(255),
                picture_address VARCHAR(255),
                radiograph_address VARCHAR(255),
                decimal_list JSON
            )
        """
        cursor.execute(create_table_query)
        print(f"Table Testing1 created successfully")
    except Error as e:
        print(f"The error '{e}' occurred while creating or checking the table")


# save Records into DB
def save_data_to_db(connection,cursor, data):
    try:

        insert_data_query = f"INSERT INTO Testing1(name, age, gender, state, picture_address, radiograph_address, decimal_list) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        insert_data_values = (
            data["name"],
            data["age"],
            data["gender"],
            data["state"],
            data["picture_address"],
            data["radiograph_address"],
            json.dumps(data["dental_features"])  # Convert list to JSON string
        )
        cursor.execute(insert_data_query, insert_data_values)


        connection.commit()
        print("Data saved successfully")
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
           
 
 
            
def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed")


# create users table




def db_operations(name, age, gender, state, pic_address, radiograph_address, extracted_features):
    create_database()
    connection = create_connection()
    cursor = connection.cursor()
    if connection:
        create_table(connection, cursor)

        data = {
            "name": name,
            "age": age,
            "gender": gender,
            "state": state,
            "picture_address": pic_address,
            "radiograph_address": radiograph_address,
            "dental_features": extracted_features
        }

        save_data_to_db(connection, cursor, data)
        close_connection(connection, cursor)

# if __name__ == "__main__":

#     db_operations("George", 35, "Male", "Taxas", "/path/to/picture.jpg", "/path/to/radiograph.jpg", Extracted_features)
