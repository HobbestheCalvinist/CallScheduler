import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('call_schedule.db')

# Create a cursor
cursor = conn.cursor()

# Create a table to store the information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS callers (
        id INTEGER PRIMARY KEY,
        group_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone_number TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS daysofweek (
        id INTEGER PRIMARY KEY,
        group_name TEXT NOT NULL,
        days_of_week TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
