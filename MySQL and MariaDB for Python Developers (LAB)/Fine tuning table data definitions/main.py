import sqlite3
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Shmuokh001",
    database="ine"
)

cur = conn.cursor()

def table_schema(table_name):
    import pandas as pd
    pd.set_option('display.max_columns', None)
    cur.execute(f"SHOW columns FROM {table_name}")
    info_cols = [c[0] for c in cur.description]
    schema = cur.fetchall()
    df = pd.DataFrame(schema, columns=info_cols)
    # Nullable as Bool value
    df['Null'] = df.Null == 'YES'
    return df

cur.execute("DROP TABLE IF EXISTS Tweets_new;")
cur.execute("CREATE TABLE Tweets_new SELECT * FROM Tweets;")
conn.commit()

schema = table_schema('Tweets_new')
print(schema)

categories = dict()
for col in schema.Field:
    cur.execute(f"SELECT count(DISTINCT {col}) FROM Tweets_new;")
    num = cur.fetchone()[0]
    print(f"{col} has {num} distinct values")
    if num < 10:
        cur.execute(f"SELECT DISTINCT {col} FROM Tweets_new;")
        categories[col] = [t[0] for t in cur]

cur.execute("UPDATE Tweets_new SET airline_sentiment_gold = NULL WHERE airline_sentiment_gold = '';")
cur.execute("SELECT DISTINCT airline_sentiment_gold FROM Tweets_new;")
cur.fetchall()

sql_enum_sentiment = """
ALTER TABLE Tweets_new
MODIFY COLUMN airline_sentiment ENUM ('negative', 'positive', 'neutral');
"""
cur.execute(sql_enum_sentiment)

sql_enum_sentiment_gold = """
ALTER TABLE Tweets_new
MODIFY COLUMN airline_sentiment_gold ENUM ('negative', 'positive', 'neutral');
"""
cur.execute(sql_enum_sentiment_gold)

sql_airlines = """
ALTER TABLE Tweets_new
MODIFY COLUMN airline 
  ENUM ('Virgin America', 'Southwest',  'Delta', 'American',  'US Airways', 'United');
"""
cur.execute(sql_airlines)

print(table_schema('Tweets_new'))
conn.commit()



cur.execute("DROP TABLE IF EXISTS Tweets_new")
cur.execute("CREATE TABLE Tweets_new SELECT * FROM Tweets;")
conn.commit()

sql_airlines = [
  "ALTER TABLE Tweets_new MODIFY COLUMN airline CHAR(50)",
  "ALTER TABLE Tweets_new MODIFY COLUMN user_timezone CHAR(50)"
]
for sql in sql_airlines:
    cur.execute(sql)
sql_airlines = """
CREATE TABLE airlines (
    airline CHAR(50) PRIMARY KEY,  -- alternate compact key definition
    description TEXT DEFAULT NULL
    );
"""
cur.execute('DROP TABLE IF EXISTS airlines')
cur.execute(sql_airlines)

sql_timezones = """
CREATE TABLE timezones (
    timezone CHAR(50) PRIMARY KEY,
    description TEXT DEFAULT NULL
    );
"""
cur.execute('DROP TABLE IF EXISTS timezones')
cur.execute(sql_timezones)

sql_populate_airlines = """
INSERT INTO airlines (airline)
SELECT DISTINCT airline FROM Tweets_new;
"""
cur.execute(sql_populate_airlines)
sql_populate_timezones = """
INSERT INTO timezones (timezone)
SELECT DISTINCT user_timezone FROM Tweets_new
WHERE user_timezone IS NOT NULL;
"""

cur.execute(sql_populate_timezones)
conn.commit()

sql_airline_constraint = """
ALTER TABLE Tweets_new
ADD FOREIGN KEY (airline) 
REFERENCES airlines(airline)
ON DELETE CASCADE;
"""
cur.execute(sql_airline_constraint)
conn.commit()

# After alteration need to close cursor and get new one
cur.close()
cur = conn.cursor()
sql_timezone_constraint = """
ALTER TABLE Tweets_new
ADD FOREIGN KEY (user_timezone)
REFERENCES timezones(timezone)
ON DELETE SET NULL;
"""
cur.execute(sql_timezone_constraint)
conn.commit()
import pandas as pd
print(cur.execute("SHOW INDEXES FROM Tweets_new;"))
pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description]).T