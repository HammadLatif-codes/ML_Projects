import mysql.connector
from mysql.connector import Error




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





# Function to fetch all data with specific columns
def fetch_data():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        select_data_query = "SELECT name, age, gender, state, picture_address FROM Testing1"
        cursor.execute(select_data_query)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return None
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return None


# Function to fetch data based on age
def fetch_data_by_age(age, comparison_operator = '='):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if comparison_operator == '=':
            select_data_query = "SELECT name, age, gender, state, picture_address FROM Testing1 WHERE age = %s"
        elif comparison_operator == '<':
            select_data_query = "SELECT name, age, gender, state, picture_address FROM Testing1 WHERE age < %s"
        elif comparison_operator == '>':
            select_data_query = "SELECT name, age, gender, state, picture_address FROM Testing1 WHERE age > %s"
        else:
            print("Invalid comparison operator. Please use '=', '<', or '>'")
            return None
        cursor.execute(select_data_query, (age,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return None
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return None


# Function to fetch data based on gender
def fetch_data_by_gender( gender):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        select_data_query = "SELECT name, age, gender, state, picture_address FROM Testing1 WHERE gender = %s"
        cursor.execute(select_data_query, (gender,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return None
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return None


# Function to fetch data based on state
def fetch_data_by_state( state):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        select_data_query = "SELECT name, age, gender, state, picture_address FROM Testing1 WHERE state = %s"
        cursor.execute(select_data_query, (state,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return None
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return None


if __name__ == "__main__":
    records = fetch_data()
    # records = fetch_data_by_age(24,'=')
    # records = fetch_data_by_gender('female')
    # records = fetch_data_by_state('islamabad')
    print(records)