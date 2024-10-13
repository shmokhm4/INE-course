from datetime import time
import mysql.connector
import sqlite3
from pprint import pprint
from threading import Thread
from time import sleep, time  # Import time for timing
from queue import Queue

myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Shmuokh001",
    database="ine"
)

myCursor = myDB.cursor()

# ------------------ PART 1 ------------------
# Move data into MySQL

print("------------------ PART 1 ------------------")

# Create the table with cursor#1
sql_create = """
CREATE TABLE IF NOT EXISTS Tweets (
    tweet_id DECIMAL(18) PRIMARY KEY,
    airline_sentiment TEXT,
    airline_sentiment_confidence REAL,
    negativereason TEXT,
    negativereason_confidence REAL,
    airline TEXT,
    airline_sentiment_gold TEXT,
    name TEXT,
    negativereason_gold TEXT,
    retweet_count INT,
    text TEXT,
    tweet_coord TEXT,
    tweet_created TIMESTAMP,
    tweet_location TEXT,
    user_timezone TEXT
);
"""

myCursor.execute("DROP TABLE IF EXISTS Tweets;")
myCursor.execute(sql_create)
myDB.commit()

conect_data = sqlite3.connect('Airline-Tweets.sqlite')
myCursor2 = conect_data.cursor()
myCursor2.execute("SELECT * FROM Tweets")

# SQLite gives output an empty string rather than None. so I will fix it

# Offset indicated in SQLite
myCursor.execute("SET time_zone = '-08:00';")
sql_insert = """
INSERT INTO Tweets 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for src_row in myCursor2:
    row = [data or None for data in src_row]
    timestamp = row[12][:19]  # Omit offset portion
    row[12] = timestamp
    row = tuple(row)
    myCursor.execute(sql_insert, row)

myDB.commit()

myCursor.execute("SELECT * FROM Tweets LIMIT 2;")
cols = [c[0] for c in myCursor.description]
for row in myCursor:
    pprint(dict(zip(cols, row)))

# ------------------ PART 2 ------------------
# Skipping problem data when loading

print("------------------ PART 2 ------------------")

sql_create_issues = """
CREATE TABLE data_issues (
    tweet_id DECIMAL(18) PRIMARY KEY, 
    message TEXT
    );
"""
# Clear out old content of dest
myCursor.execute('DROP TABLE IF EXISTS data_issues;')
myCursor.execute(sql_create_issues)
myCursor.execute('DROP TABLE IF EXISTS Tweets;')
myCursor.execute(sql_create)
myDB.commit()

qsize = 20
pool = Queue(maxsize=qsize)
for _ in range(qsize):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Shmuokh001",
        database="ine"
    )
    pool.put(conn)

def add_row(pool, row):
    conn = pool.get()
    cursor = conn.cursor()
    try:
        row = list(row)
        row[12] = row[12][:19]  # Omit offset portion
        cursor.execute(sql_insert, tuple(row))
    except Exception as err:
        conn.rollback()
        cursor.execute("INSERT INTO data_issues VALUES (%s, %s);",
                       (row[0], str(err)))
    finally:
        conn.commit()
        pool.put(conn)

# Measure the time taken
start_time = time()

myCursor2.execute("SELECT * FROM Tweets")

threads = []
for row in myCursor2:
    t = Thread(target=add_row, args=(pool, row))
    t.start()
    threads.append(t)

# Ensure all threads are completed
for t in threads:
    t.join()

end_time = time()

# Print the execution time
print(f"Data migration completed in: {end_time - start_time:.2f} seconds\n")

# Print the total number of records in the Tweets table
myCursor.execute('SELECT count(*) FROM Tweets;')
tweet_count = myCursor.fetchone()[0]
print(f"Total records inserted into 'Tweets' table: {tweet_count}\n")

# Print issues found during data insertion (up to 5 for clarity)
myCursor.execute("SELECT * FROM data_issues LIMIT 5;")
issues = myCursor.fetchall()
if issues:
    print(f"Issues encountered during data migration (showing up to 5):")
    for issue in issues:
        tweet_id, error_message = issue
        print(f"- Tweet ID {tweet_id}: {error_message}")
else:
    print("No data issues encountered.\n")

# Print the total number of records in the data_issues table
myCursor.execute("SELECT count(*) FROM data_issues;")
issue_count = myCursor.fetchone()[0]
print(f"Total records in 'data_issues' table: {issue_count}")
