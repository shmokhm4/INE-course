import pandas as pd
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Shmuokh001",
    database="ine"
)

cur = conn.cursor()

sql = """
SELECT airline, avg(airline_sentiment_confidence), avg(negativereason_confidence)
FROM Tweets
GROUP BY airline;
"""
cur.execute(sql)
print("")
print(pd.DataFrame(cur.fetchall(), columns=['airline', 'avg_sentiment_conf', 'avg_neg_conf']))
print("")
sql_conf = """
CREATE OR REPLACE VIEW airline_sentiment (
    airline, mean, gmean, midrange) AS 
SELECT airline, 
       avg(airline_sentiment_confidence),
       exp(sum(log(airline_sentiment_confidence)) / count(airline_sentiment_confidence)),
       (max(airline_sentiment_confidence) + min(airline_sentiment_confidence)) / 2
FROM Tweets
GROUP BY airline;
"""
cur.execute(sql_conf)
cur.execute("SELECT * FROM airline_sentiment")

print(pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description]))
print("")
results = {}
cur.execute("SELECT DISTINCT airline FROM Tweets")
for row in cur.fetchall():
    airline = row[0]
    newcur = conn.cursor()
    newcur.execute(f"SELECT count(*) FROM Tweets WHERE airline='{airline}'")
    mid = newcur.fetchone()[0] // 2
    sql = (f"SELECT airline_sentiment_confidence "
           f"FROM Tweets LIMIT 1 OFFSET {mid}")
    newcur.execute(sql)
    results[airline] = newcur.fetchone()[0]

print(results)