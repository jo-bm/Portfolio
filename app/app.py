from flask import Flask, render_template,request,Response,url_for
import pandas as pd
import csv,random
from testdb import *


#db connect 

conn()
execute_mysql_command('use testdb')




def insert_data_from_csv_to_db():
    # Connect to the database
    cnx = conn()

    # Open the CSV file and read its contents
    with open('parties.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
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

result = execute_mysql_command("SELECT COUNT(*) FROM parties")
count = result[0][0]

if count == 0:
    print("The parties table is empty")
    insert_data_from_csv_to_db()
    print("Data added to db")


app = Flask(__name__)


@app.route('/')
def index():
# Connect to the MySQL database
    db = conn()
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # Retrieve the party names from the MySQL table
    cursor.execute("SELECT party_name FROM parties")
    party_names = [row[0] for row in cursor.fetchall()]

    # Close the cursor and database connection
    cursor.close()
    db.close()

    return render_template("index.html", party_names=party_names)



# @app.route('/party', methods=['POST'])
# def print_party():
#     data = request.get_json()
#     party = data["party"]
#     print(party)
#     return ""
@app.route('/<party_name>')
def party(party_name):
    # Connect to the database
    cnx = conn()

    # Retrieve the party name and platform from the parties table
    cursor = cnx.cursor()
    select_query = "SELECT party_name, platform FROM parties WHERE id = %s"
    party_number = int(party_name.replace('party_', '')) + 1
    cursor.execute(select_query, (party_number,))
    result = cursor.fetchone()

    # Close the database connection
    cursor.close()
    cnx.close()

    # Generate random IDs
    ids_list = ['177876653','035686674','672477031','413743345','093175180','468389937','087926721','298250838','328664701','798332409','398759266','601638695','681278263','510684194','979533981','640309290','432901288','855708863','301398160']
    random_ids = [random.choices(ids_list, k=5)]



    # Pass the retrieved data and the random IDs to the template
    return render_template("party.html", party_name=result[0], platform=result[1], random_ids=random_ids)

@app.route('/vote', methods=['POST'])
def vote():
    # Get the ID and party name from the form data
    user_id = request.form.get('id', '')
    party_name = request.form.get('party_name', '')

    # Connect to the database
    cnx = conn()
    cursor = cnx.cursor()

    # Check if the user exists in the database and is eligible to vote
    query = "SELECT vote_entitlement, voted FROM tbl_user WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if not result:
        response = 'User not found'
    elif result[0] != 'true':
        response = 'User not eligible to vote'
    elif result[1] == 'true':
        response = 'User has already voted'
    else:
        # Update the 'voted' column to indicate that the user has voted
        query = "UPDATE tbl_user SET voted = 'true' WHERE user_id = %s"
        cursor.execute(query, (user_id,))

        # Increment the vote count for the party in the parties_statistic table
        query = "SELECT votes_number FROM parties_statistic WHERE party_name = %s"
        cursor.execute(query, (party_name,))
        result = cursor.fetchone()

        if not result:
            # Insert a new row for the party with a vote count of 1
            query = "INSERT INTO parties_statistic (party_name, votes_number) VALUES (%s, 1)"
            cursor.execute(query, (party_name,))
        else:
            # Increment the vote count for the party
            vote_count = int(result[0]) + 1
            query = "UPDATE parties_statistic SET votes_number = %s WHERE party_name = %s"
            cursor.execute(query, (str(vote_count), party_name))

        cnx.commit()
        response = 'true'

    cursor.close()
    cnx.close()

    return response



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'שם משתמש או סיסמה לא נכונים..(admin/admin) '
        else:
            db = conn()
            # Create a cursor object to execute SQL queries
            cursor = db.cursor()

            # Retrieve the party names from the MySQL table
            cursor.execute("SELECT party_name FROM parties")
            party_names = [row[0] for row in cursor.fetchall()]

            # Close the cursor and database connection
            cursor.close()
            db.close()

            return render_template('adminspage.html', error=error, party_names=party_names)
    return render_template('login.html', error=error)


@app.route('/download-csv')
def download_csv():
    # create a database connection
    db = conn()
    
    # execute a SELECT query to retrieve the data
    cursor = db.cursor()
    cursor.execute('SELECT * FROM tbl_user')
    rows = cursor.fetchall()
    
    # create the CSV file and write the data to it
    output = []
    for row in rows:
        output.append([str(col) for col in row])
    
    with open('static/parties.csv', 'w', newline='') as csvfile:
        column_names = ['','user_id', 'vote_entitlement', 'voted']
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerows(output)

    # close the database connection
    cursor.close()
    db.close()

    # serve the file for download
    with open('static/parties.csv', 'r') as csvfile:
        data = csvfile.read()
        response = Response(data, mimetype='text/csv', headers={'Content-disposition': 'attachment; filename=parties.csv'})
        return response
@app.route('/download-parties-csv')
def download_parties_csv():
    # create a database connection
    db = conn()
    
    # execute a SELECT query to retrieve the data
    cursor = db.cursor()
    cursor.execute('SELECT * FROM parties_statistic')
    rows = cursor.fetchall()
    
    # create the CSV file and write the data to it
    output = []
    for row in rows:
        output.append([str(col) for col in row])
    
    with open('static/parties.csv', 'w', newline='') as csvfile:
        column_names = ['row', 'party_name', 'votes_number']
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerows(output)

    # close the database connection
    cursor.close()
    db.close()

    # serve the file for download
    with open('static/parties.csv', 'r') as csvfile:
        data = csvfile.read()
        response = Response(data, mimetype='text/csv', headers={'Content-disposition': 'attachment; filename=parties.csv'})
        return response

@app.route('/add-party', methods=['POST'])
def add_party():
    party_name = request.form['party_name']
    party_platform = request.form['party_platform']

    # create a database connection
    db = conn()
    
    # execute an INSERT query to add the new party to the database
    cursor = db.cursor()
    cursor.execute('INSERT INTO parties (party_name, platform) VALUES (%s, %s)', (party_name, party_platform))
    db.commit()

    # close the database connection
    cursor.close()
    db.close()

    return 'Party added successfully'


#####
@app.route('/delete-party', methods=['POST'])
def delete_party():
    party_name = request.form['party_name']

    # create a database connection
    db = conn()
    
    # execute a DELETE query to remove the party from the database
    cursor = db.cursor()
    cursor.execute('DELETE FROM parties WHERE party_name=%s', (party_name,))
    db.commit()

    # close the database connection
    cursor.close()
    db.close()

    return 'Party deleted successfully'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


