# First lab in the course: Working with the Python DBA and MySQL💫
In this project, i will practice using Python's DB-API to access MySQL

## Features
- SQLite to MySQL Data Migration: Automatically migrates data from a SQLite table to a MySQL database.
- Multithreaded Processing: Uses multithreading to speed up data insertion by processing multiple rows concurrently.
- Performance Tracking: Prints the total time taken for data migration.

## Sample output:
```bash
------------------ PART 1 ------------------
{'airline': 'Delta',
 'airline_sentiment': 'neutral',
 'airline_sentiment_confidence': 1.0,
 'airline_sentiment_gold': None,
 'name': 'JetBlueNews',
 'negativereason': None,
 'negativereason_confidence': None,
 'negativereason_gold': None,
 'retweet_count': None,
 'text': "@JetBlue's new CEO seeks the right balance to please passengers and "
         'Wall ... - Greenfield Daily Reporter http://t.co/LM3opxkxch',
 'tweet_coord': None,
 'tweet_created': datetime.datetime(2015, 2, 16, 23, 36, 5),
 'tweet_id': Decimal('567588278875213824'),
 'tweet_location': 'USA',
 'user_timezone': 'Sydney'}
{'airline': 'Delta',
 'airline_sentiment': 'negative',
 'airline_sentiment_confidence': 1.0,
 'airline_sentiment_gold': None,
 'name': 'nesi_1992',
 'negativereason': "Can't Tell",
 'negativereason_confidence': 0.6503,
 'negativereason_gold': None,
 'retweet_count': None,
 'text': '@JetBlue is REALLY getting on my nerves !! 😡😡 #nothappy',
 'tweet_coord': None,
 'tweet_created': datetime.datetime(2015, 2, 16, 23, 43, 2),
 'tweet_id': Decimal('567590027375702016'),
 'tweet_location': 'undecided',
 'user_timezone': 'Pacific Time (US & Canada)'}
------------------ PART 2 ------------------
Data migration completed in: 37.12 seconds

Total records inserted into 'Tweets' table: 10416

Issues encountered during data migration (showing up to 5):
- Tweet ID 567588278875213824: 1265 (01000): Data truncated for column 'negativereason_confidence' at row 1
- Tweet ID 567634106058821632: 1265 (01000): Data truncated for column 'negativereason_confidence' at row 1
- Tweet ID 567643252753694721: 1265 (01000): Data truncated for column 'negativereason_confidence' at row 1
- Tweet ID 567655489119326209: 1265 (01000): Data truncated for column 'negativereason_confidence' at row 1
- Tweet ID 567667301067915264: 1265 (01000): Data truncated for column 'negativereason_confidence' at row 1
Total records in 'data_issues' table: 4069
