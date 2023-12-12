from flask import Flask, redirect, url_for, request, render_template, session, jsonify
import sqlite3
import os

app = Flask(__name__)

# Define the path to the SQLite database file
db_file = 'call_schedule.db'

# Check if the database file doesn't exist
if not os.path.isfile(db_file):
    # If the database doesn't exist, create it using the 'createdb.py' script
    import subprocess
    subprocess.call(['python', 'createdb.py'])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_to_call_list', methods=['POST'])
def add_to_call_list():
    data = request.json  # Assuming data is sent as JSON
    group_name = data.get('group_name')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')

    conn = sqlite3.connect('call_schedule.db')
    cursor = conn.cursor()

    # Check if the group name already exists in the database
    cursor.execute("SELECT * FROM callers WHERE group_name=? and first_name = ? and last_name = ?", 
                   (group_name, first_name, last_name,))
    existing_record = cursor.fetchone()

    if existing_record:
        # If the group name already exists, update the caller's information
        cursor.execute("UPDATE callers SET first_name = ?, last_name = ?, phone_number = ? WHERE group_name = ?",
                       (first_name, last_name, phone_number, group_name))
    else:
        # If the group name doesn't exist, insert the data into the database
        cursor.execute("INSERT INTO callers (group_name, first_name, last_name, phone_number) VALUES (?, ?, ?, ?)",
                       (group_name, first_name, last_name, phone_number))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Data added to the database'})

@app.route('/remove_from_call_list', methods=['POST'])
def remove_from_call_list():
    data = request.json  # Assuming data is sent as JSON
    group_name = data.get('group_name')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    conn = sqlite3.connect('call_schedule.db')
    cursor = conn.cursor()

    # If the group name already exists, update the caller's information
    cursor.execute("DELETE from callers where first_name = ? and last_name = ? and group_name = ?",
                    (first_name, last_name, group_name))


    conn.commit()
    conn.close()

    return jsonify({'message': 'Data removed from the database'})


@app.route('/save_to_days_of_week', methods=['POST'])
def save_to_days_of_week():
    data = request.json  # Assuming data is sent as JSON
    group_name = data.get('group_name')
    days_of_week = str(data.get('selected_days'))

    conn = sqlite3.connect('call_schedule.db')
    cursor = conn.cursor()

    # Check if the group name already exists in the database
    cursor.execute("SELECT group_name FROM daysofweek WHERE group_name=?", (group_name,))
    existing_group = cursor.fetchone()

    if existing_group:
        # If the group name already exists, update the days_of_week for that group
        cursor.execute("UPDATE daysofweek SET days_of_week = ? WHERE group_name = ?", (days_of_week, group_name))
    else:
        # If the group name doesn't exist, insert the data into the database
        cursor.execute("INSERT INTO daysofweek (group_name, days_of_week) VALUES (?, ?)", (group_name, days_of_week))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Data added to the database'})



@app.route('/load_callers_from_db', methods=['POST'])
def load_callers_from_db():
    
    data = request.json  # Assuming data is sent as JSON
    group_name = str(data.get('group_name'))
    
    # Retrieve data from the database and generate the call schedule
    conn = sqlite3.connect('call_schedule.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM callers WHERE group_name=?", (group_name,))
    currsorData = cursor.fetchall()
    print (currsorData)
    conn.close()
    callers = []

    for row in currsorData:
        id, group_name, first_name, last_name, phone_number = row
        callers.append({
            'id': id,
            'group_name': group_name,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number
        })

    print (callers)
    # Close the database connection
    conn.close()

    # Convert the data to a JSON object

    json_data = jsonify(callers)

    return json_data


@app.route('/load_daysofweek_from_db', methods=['POST'])
def load_daysofweek_from_db():
    
    data = request.json  # Assuming data is sent as JSON
    group_name = data.get('group_name')
    
    # Retrieve data from the database and generate the call schedule
    conn = sqlite3.connect('call_schedule.db')
    cursor = conn.cursor()

    cursor.execute("SELECT group_name, days_of_week FROM daysofweek WHERE group_name=?", (group_name,))

    data = cursor.fetchall()

    returnValue = []

    for row in data:
        group_name, days_of_week = row
        strdays_of_week = str(days_of_week)
        returnValue.append(f'Group: {group_name}, daysofweek: {strdays_of_week}')

    conn.close()
    return jsonify({'daysofweek': returnValue})


if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)


