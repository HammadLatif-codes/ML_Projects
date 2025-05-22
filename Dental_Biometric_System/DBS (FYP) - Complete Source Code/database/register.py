#  USE forensic_dental_biometrics;
#  SHOW TABLES;
#  

import mysql.connector
from mysql.connector import Error

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




def create_users_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_table_query)
    print("Table 'users' created successfully.")

def insert_user_data(connection,cursor, user_data):
    insert_query = """
    INSERT INTO users (username, password, role) VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_query, user_data)
    connection.commit()
    return True

def close_connection(cursor, connection):
    cursor.close()
    connection.close()

def sign_up(username, password):
    connection = create_connection()
    cursor = connection.cursor()

    create_users_table(cursor)

    user_data = [
        (username, password, "Forensic officer"),
    ]
    
  
    
    if insert_user_data(connection,cursor, user_data):
        close_connection(cursor, connection)
        return True
    else:
        close_connection(cursor, connection)
        return False 

    



# validate user during sign in
def validate_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    select_query = """
    SELECT role FROM users WHERE username = %s AND password = %s
    """
    cursor.execute(select_query, (username, password))
    result = cursor.fetchone()

    if result:
        role = result[0]
        print(f"User found. Role: {role}")
        return role
    else:
        print("User not found.")
        return None