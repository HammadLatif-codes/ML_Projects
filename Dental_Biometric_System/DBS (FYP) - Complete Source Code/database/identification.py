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



import json

def fetch_radiographs_features():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        fetch_data_query = "SELECT id, decimal_list FROM Testing1"
        cursor.execute(fetch_data_query)
        rows = cursor.fetchall()

        data_list = []
        for row in rows:
            data = {
                "id": row[0],
                "decimal_list": json.loads(row[1])  # Convert JSON string to list
            }
            data_list.append(data)

        return data_list

    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return None
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return None




import numpy as np

def find_matching_ids(data_list, features_list):
    similarity_threshold=0.9
    matched_ids_list = []
    for data in data_list:
        decimal_list = data["decimal_list"]
        # Perform similarity search


        # Calculate similarity score using dot product for cosine similarity
        similarity_score = np.dot(decimal_list, features_list) / (np.linalg.norm(decimal_list) * np.linalg.norm(features_list))
        # Check if the similarity score is above the threshold
        if similarity_score > similarity_threshold:
            matched_ids_list.append(data["id"])



    return matched_ids_list






# Function to fetch data from database based on ID
def fetch_data_by_id(id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        select_data_query = "SELECT name, age, gender, state, picture_address FROM Testing1 WHERE id = %s"
        cursor.execute(select_data_query, (id,))
        record = cursor.fetchone()
        if record:
            data = {
                "name": record[0],
                "age": record[1],
                "gender": record[2],
                "state": record[3],
                "picture_address": record[4]
            }
            return data
        else:
            return False
    except mysql.connector.Error as e:
        print(f"MySQL Connector Error: {e.msg}")
        print(f"MySQL Connector Error Code: {e.errno}")
        print(f"MySQL Connector SQL State: {e.sqlstate}")
        return False
    except Exception as ex:
        print(f"Other Error: {str(ex)}")
        return False

# Function to fetch data from database based on list of IDs
def fetch_data_by_ids( id_list):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        data_list = []
        for id in id_list:
            data = fetch_data_by_id(id)
            if data:
                data_list.append(data)
        return data_list
    except Exception as ex:
        print(f"Error fetching data for IDs: {str(ex)}")
        return []




if __name__ == "__main__":
    data = fetch_radiographs_features()
    