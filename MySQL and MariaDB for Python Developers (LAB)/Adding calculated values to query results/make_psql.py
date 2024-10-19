# A possible way of creating the needed MySQL table.
import sqlite3
import mysql

# Connect to the MySQL database
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Shmuokh001",
    database="ine"
)

myCursor = myDB.cursor()

# create MySQL table
sql_create_tweets = '''
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
'''
myCursor.execute("DROP TABLE IF EXISTS Tweets;")
myCursor.execute(sql_create_tweets)
myCursor.commit()

con_src = sqlite3.connect('Airline-Tweets.sqlite') 
cur_src = con_src.cursor()
cur_src.execute("SELECT * FROM Tweets")

# Offset indicated in SQLite
myCursor.execute("SET time_zone = '-08:00';")

sql_insert = """
INSERT INTO Tweets 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
for src_row in cur_src:
    row = [data or None for data in src_row]
    timestamp = row[12][:19]  # Omit offset portion
    row[12] = timestamp
    row = tuple(row)
    myCursor.execute(sql_insert, row)
    
myDB.commit()

from pprint import pprint
myCursor.execute("SELECT * FROM Tweets LIMIT 2;")
cols = [c[0] for c in myCursor.description]
for row in myCursor:
    pprint(dict(zip(cols, row)))