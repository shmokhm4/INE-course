# Second lab in the course: Timing and comparing adapter performance💫
This project demonstrates how to compare the performance of different MySQL adapters for Python, namely aiomysql, pymysql, and mysql.connector, by measuring CPU times and wall time for queries executed on a MySQL database.

## Features ✨
- Multiple Adapter Support: Measure performance for three different MySQL adapters:
1. `aiomysql:` An asynchronous MySQL driver for Python. 🚀
2. `pymysql:` A pure-Python MySQL client. 🐍
3. `mysql.connector:` The official MySQL driver provided by Oracle. 🏢

- Performance Metrics:
1. `CPU Times:` Breakdown of user and system CPU times for each adapter. ⏱️
2. `Wall Time:` Total elapsed time for executing queries, including I/O waits. ⏳

## Sample output
```bash
------------------ PART 1 ------------------
CPU times: user 0.25 s, sys: 0.12 s, total: 0.38 s
Wall time: 4.21 s
------------------ PART 2 ------------------
------------------ Timing aiomysql (async) ------------------
CPU times (async): user 0.02 s, sys: 0.02 s, total: 0.03 s
Wall time (async): 0.03 s
Number of results: 1405
------------------ Timing pymysql ------------------
CPU times (pymysql): user 0.02 s, sys: 0.00 s, total: 0.02 s
Wall time (pymysql): 0.06 s
Number of results: 1405
------------------ Timing mysql.connector ------------------
CPU times (mysql.connector): user 0.02 s, sys: 0.00 s, total: 0.02 s
Wall time (mysql.connector): 0.03 s
Number of results: 1405
