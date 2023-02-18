from flask import Flask, render_template,request,Response,url_for
import pandas as pd
import csv,random,logging,re
from testdb import *



conn()
execute_mysql_command('use testdb')

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='applogs.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


#initdb()
# initdb()

# Check if the parties table is empty
result = execute_mysql_command("SELECT COUNT(*) FROM parties")
count = result[0][0]

if count == 0:
    print("The parties table is empty")
    insert_data_from_csv_to_db()
    print("Data added to db")




# Log a message
#logging.info('This is an example log message.')

@app.route('/')
def index():
    db = conn()
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()


    cursor.execute("SELECT party_name FROM parties")
    party_names = [row[0] for row in cursor.fetchall()]

    cursor.close()
    db.close()

    return render_template("index.html", party_names=party_names)



@app.route('/<party_name>')
def party(party_name):

    if (re.match(r"party_\d+", party_name)) :
        # Connect to the database
        cnx = conn()

        # Retrieve the party name and platform from the parties table
        cursor = cnx.cursor()
        select_query = "SELECT party_name, platform FROM parties WHERE id = %s"
        some = int(party_name.split('_')[1]) + 1
        
        cursor.execute(select_query, (int(some),))
        result = cursor.fetchone()

        # Close the database connection
        cursor.close()
        cnx.close()

        # Generate random IDs
        ids_list = ['964501563','177876653','035686674','672477031','413743345','093175180','468389937','087926721','298250838','328664701','798332409','398759266','601638695','681278263','510684194','979533981','640309290','432901288','855708863','301398160']
        random_ids = [random.choices(ids_list, k=5)]

        # Pass the retrieved data and the random IDs to the template
        return render_template("party.html", party_name=result[0], platform=result[1], random_ids=random_ids)

    else:
        #or party_name == '' or party_name == 'favicon.ico'
        return render_template('404.html'), 404


@app.route('/vote', methods=['POST'])
def vote():
    user_id = request.form.get('id', '')
    party_name = request.form.get('party_name', '')

    cnx = conn()
    cursor = cnx.cursor()

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
            cursor = db.cursor()

            # Retrieve the party names from the MySQL table
            cursor.execute("SELECT party_name FROM parties")
            party_names = [row[0] for row in cursor.fetchall()]

            cursor.close()
            db.close()

            return render_template('adminspage.html', error=error, party_names=party_names)
    return render_template('login.html', error=error)


@app.route('/download-csv')
def download_csv():
    db = conn()
    
    cursor = db.cursor()
    cursor.execute('SELECT * FROM tbl_user')
    rows = cursor.fetchall()
    
    output = []
    for row in rows:
        output.append([str(col) for col in row])
    
    with open('static/parties.csv', 'w', newline='') as csvfile:
        column_names = ['','user_id', 'vote_entitlement', 'voted']
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerows(output)

    cursor.close()
    db.close()

    with open('static/parties.csv', 'r') as csvfile:
        data = csvfile.read()
        response = Response(data, mimetype='text/csv', headers={'Content-disposition': 'attachment; filename=parties.csv'})
        return response
    

@app.route('/download-parties-csv')
def download_parties_csv():
    db = conn()
    
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

    db = conn()
    
    cursor = db.cursor()
    cursor.execute('INSERT INTO parties (party_name, platform) VALUES (%s, %s)', (party_name, party_platform))
    db.commit()

    cursor.close()
    db.close()

    return 'Party added successfully'



@app.route('/delete-party', methods=['POST'])
def delete_party():
    party_name = request.form['party_name']

    db = conn()
    
    # execute a DELETE query to remove the party from the database
    cursor = db.cursor()
    cursor.execute('DELETE FROM parties WHERE party_name=%s', (party_name,))
    db.commit()

    cursor.close()
    db.close()

    return 'Party deleted successfully'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
