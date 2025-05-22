import mysql.connector
from mysql.connector import Error

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

def table_exists(cursor, table_name):
    try:
        cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
        return True
    except Error:
        return False

def create_table(connection):
    try:
        cursor = connection.cursor()

        table_name = "Testing7"
        
        if table_exists(cursor, table_name):
            print(f"Table '{table_name}' already exists")
        else:
            create_table_query = f"""
                CREATE TABLE {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    age INT,
                    gender VARCHAR(10),
                    state VARCHAR(255),
                    picture_address VARCHAR(255),
                    radiograph_address VARCHAR(255)
                )
            """
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully")
    except Error as e:
        print(f"The error '{e}' occurred while creating or checking the table")

def save_data_to_db(connection, data):
    try:
        cursor = connection.cursor()
        insert_data_query = f"INSERT INTO Testing7(name, age, gender, state, picture_address, radiograph_address) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_data_values = (
            data["name"],
            data["age"],
            data["gender"],
            data["state"],
            data["picture_address"],
            data["radiograph_address"]
        )
        cursor.execute(insert_data_query, insert_data_values)
        cursor.fetchall()  # Fetch the result to consume it
        connection.commit()
        print("Data saved successfully")
    except Error as e:
        print(f"The error '{e}' occurred while saving the data")

def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed")

def db_operations(name, age, gender, state, pic_address, radiograph_address):
    create_database()
    connection = create_connection()
    if connection:
        create_table(connection)

        data = {
            "name": name,
            "age": age,
            "gender": gender,
            "state": state,
            "picture_address": pic_address,
            "radiograph_address": radiograph_address
        }

        save_data_to_db(connection, data)
        close_connection(connection)

if __name__ == "__main__":
    db_operations("Hamza", 24, "Male", "Islamabad", "/path/to/picture.jpg", "/path/to/radiograph.jpg")
