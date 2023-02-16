#pip install mysql-connector-python 
import mysql.connector

# connect to the db
def conn():
    return mysql.connector.connect(
    user='root', 
    password='password', 
    host='172.27.0.2', 
    port=3306, 
    database='testdb'
    )



#general function to run command

def execute_mysql_command(command):
    connection = conn()
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def insert_data(username, email):
    # Connect to the database

    # Create a cursor object
    connection = conn()
    cursor = connection.cursor()

    # Insert a new user into the 'users' table
    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    values = (username, email)
    cursor.execute(query, values)
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

#insert_data('frank shumer', 'shumer@example.com')


# result = execute_mysql_command(insert_user_command)
# print(result)

# # Create a table called 'users' with columns 'id', 'username', and 'email':
# create_table_command = """
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(255) NOT NULL,
#     email VARCHAR(255) NOT NULL
# );
# """

# execute_mysql_command(create_table_command)

# Print all data from the 'users' table:
# select_all_data_command = "SELECT * FROM users"
# result = execute_mysql_command(select_all_data_command)
# print(result)

# # Delete a user with a specific id from the 'users' table:
# delete_user_command = "DELETE FROM users WHERE id = 1"
# execute_mysql_command(delete_user_command)

# # Delete the 'users' table:
# drop_table_command = "DROP TABLE users"
# execute_mysql_command(drop_table_command)

# x = input()