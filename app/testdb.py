#pip install mysql-connector-python 
import mysql.connector,csv

def insert_data_from_csv_to_db():
    cnx = conn()

    with open('parties.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) 
        data_to_insert_parties = []
        data_to_insert_parties_statistic = []
        for row in csv_reader:
            party_name = row[0]
            platform = row[1]
            data_to_insert_parties.append((party_name, platform))
            data_to_insert_parties_statistic.append((party_name, 0))

    # Insert the data into the parties table
    cursor = cnx.cursor()
    insert_query_parties = "INSERT INTO parties (party_name, platform) VALUES (%s, %s)"
    cursor.executemany(insert_query_parties, data_to_insert_parties)
    cnx.commit()

    # Insert the data into the parties_statistic table
    insert_query_parties_statistic = "INSERT INTO parties_statistic (party_name, votes_number) VALUES (%s, %s)"
    cursor.executemany(insert_query_parties_statistic, data_to_insert_parties_statistic)
    cnx.commit()

    # Close the database connection
    cursor.close()
    cnx.close()


def initdb():

    # Connect to MySQL database
    mydb = conn()
    mycursor = mydb.cursor()

    # Check if parties table exists
    mycursor.execute("SHOW TABLES LIKE 'parties'")
    result = mycursor.fetchone()

    if not result:
        # Run SQL statements to create tables and insert data
        script_path = './init.sql'
        with open(script_path, 'r') as f:
            sql_statements = f.read()
        mycursor.execute(sql_statements)
        mydb.commit()

    # Close database connection
    mycursor.close()
    mydb.close()

# connect to the db
def conn():
    return mysql.connector.connect(
    user='root', 
    password='password', 
    host='db', 
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
