import mysql.connector
from collections import namedtuple
import time
import psutil  # to get both user and system times

# Connect to the MySQL database
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Shmuokh001",
    database="ine"
)

myCursor = myDB.cursor()

# ------------------ PART 1 ------------------
# Create the sample table
print("------------------ PART 1 ------------------")

sql_create = """
CREATE TABLE IF NOT EXISTS project_zipcode_geography(
    zipcode CHAR(5), 
    land_area NUMERIC(8, 3),
    water_area NUMERIC(8, 3),
    lat REAL,      
    lon REAL,
    PRIMARY KEY (zipcode)
)
"""

myCursor.execute("DROP TABLE IF EXISTS project_zipcode_geography;")
myCursor.execute(sql_create)
myDB.commit()

# Wall time: includes time spent waiting for external resources (I/O, etc.)
start_wall_time = time.time()

# CPU times: user and system
start_cpu_times = psutil.cpu_times()

fields = ('zipcode', 'ALAND', 'AWATER', 'land_area', 'water_area', 'lat', 'lon')
Data = namedtuple('Data', fields)

sql = "INSERT into project_zipcode_geography VALUES (%s, %s, %s, %s, %s);"

with open('census-zipcodes-2018.tsv') as fh:
    next(fh)  # discard header line
    for line in fh:
        row = Data(*line.strip().split('\t'))
        myCursor.execute(sql, (row.zipcode, row.land_area, row.water_area, row.lat, row.lon))

myDB.commit()

# End timing
end_wall_time = time.time()
end_cpu_times = psutil.cpu_times()

# Calculate elapsed times
elapsed_wall_time = end_wall_time - start_wall_time

# Get CPU times for user and system
user_cpu_time = end_cpu_times.user - start_cpu_times.user
sys_cpu_time = end_cpu_times.system - start_cpu_times.system
total_cpu_time = user_cpu_time + sys_cpu_time

# Print the output in the desired format
print(f"CPU times: user {user_cpu_time:.2f} s, sys: {sys_cpu_time:.2f} s, total: {total_cpu_time:.2f} s")
print(f"Wall time: {elapsed_wall_time:.2f} s")


# ------------------ PART 2 ------------------
# Timing different adapters
print("------------------ PART 2 ------------------")

import aiomysql
import asyncio
import pymysql
import nest_asyncio
nest_asyncio.apply()

sql_nested = """
SELECT zipcode
FROM project_zipcode_geography 
WHERE 10*water_area > (
    SELECT avg(land_area) FROM project_zipcode_geography )
AND 2*land_area > (
    SELECT avg(water_area) FROM project_zipcode_geography )
ORDER BY land_area + water_area;
"""

async def query():
    conn = await aiomysql.connect(host="localhost", user="root", password="Shmuokh001", db="ine", port=3306)
    cur = await conn.cursor()
    await cur.execute(sql_nested)
    results = await cur.fetchall()
    await cur.close()  # Close cursor after use
    conn.close()  # Remove await here as it's a normal sync function
    return results



# Wall and CPU times for async query (aiomysql)
print("------------------ Timing aiomysql (async) ------------------")
start_wall_time_async = time.time()
start_cpu_times_async = psutil.cpu_times()

loop = asyncio.get_event_loop()
results = loop.run_until_complete(asyncio.gather(query()))

end_wall_time_async = time.time()
end_cpu_times_async = psutil.cpu_times()

elapsed_wall_time_async = end_wall_time_async - start_wall_time_async
user_cpu_time_async = end_cpu_times_async.user - start_cpu_times_async.user
sys_cpu_time_async = end_cpu_times_async.system - start_cpu_times_async.system
total_cpu_time_async = user_cpu_time_async + sys_cpu_time_async

print(f"CPU times (async): user {user_cpu_time_async:.2f} s, sys: {sys_cpu_time_async:.2f} s, total: {total_cpu_time_async:.2f} s")
print(f"Wall time (async): {elapsed_wall_time_async:.2f} s")
print(f"Number of results: {len(results[0])}")


# Wall and CPU times for pymysql
print("------------------ Timing pymysql ------------------")
start_wall_time_pymysql = time.time()
start_cpu_times_pymysql = psutil.cpu_times()

connA = pymysql.connect(host="localhost", user="root", passwd="Shmuokh001", database="ine", port= 3306)
curA = connA.cursor()
curA.execute(sql_nested)
results = curA.fetchall()

end_wall_time_pymysql = time.time()
end_cpu_times_pymysql = psutil.cpu_times()

elapsed_wall_time_pymysql = end_wall_time_pymysql - start_wall_time_pymysql
user_cpu_time_pymysql = end_cpu_times_pymysql.user - start_cpu_times_pymysql.user
sys_cpu_time_pymysql = end_cpu_times_pymysql.system - start_cpu_times_pymysql.system
total_cpu_time_pymysql = user_cpu_time_pymysql + sys_cpu_time_pymysql

print(f"CPU times (pymysql): user {user_cpu_time_pymysql:.2f} s, sys: {sys_cpu_time_pymysql:.2f} s, total: {total_cpu_time_pymysql:.2f} s")
print(f"Wall time (pymysql): {elapsed_wall_time_pymysql:.2f} s")
print(f"Number of results: {len(results)}")


# Wall and CPU times for mysql.connector
print("------------------ Timing mysql.connector ------------------")
start_wall_time_mysql = time.time()
start_cpu_times_mysql = psutil.cpu_times()

connB = mysql.connector.connect(host="localhost", user="root", passwd="Shmuokh001", database="ine", port= 3306)
curB = connB.cursor()
curB.execute(sql_nested)
results = curB.fetchall()

end_wall_time_mysql = time.time()
end_cpu_times_mysql = psutil.cpu_times()

elapsed_wall_time_mysql = end_wall_time_mysql - start_wall_time_mysql
user_cpu_time_mysql = end_cpu_times_mysql.user - start_cpu_times_mysql.user
sys_cpu_time_mysql = end_cpu_times_mysql.system - start_cpu_times_mysql.system
total_cpu_time_mysql = user_cpu_time_mysql + sys_cpu_time_mysql

print(f"CPU times (mysql.connector): user {user_cpu_time_mysql:.2f} s, sys: {sys_cpu_time_mysql:.2f} s, total: {total_cpu_time_mysql:.2f} s")
print(f"Wall time (mysql.connector): {elapsed_wall_time_mysql:.2f} s")
print(f"Number of results: {len(results)}")
