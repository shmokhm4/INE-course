# 3th Lab in the Course: Perform database management with admin tools💫
This project focuses on performing essential database and user management tasks using MySQL administration tools. 
We will create a database, manage users, define roles, and assign specific permissions to those users,
ensuring proper access control and security.
## Features ✨
- Create and manage a MySQL database: Set up a new database and users.
- User role management: Assign different roles with specific permissions.
- Database tables management: Create multiple tables with distinct permissions for each user.

## Run 🪄
### 📝 PART 1: Database and User Creation
1. Create the Database:
```bash
mysql> CREATE DATABASE ine_project;
Query OK, 1 row affected (0.01 sec)
```
2. Create Users:
```bash
mysql> CREATE USER 'alice'@'localhost' IDENTIFIED BY 'alicepw';
Query OK, 0 rows affected (0.02 sec)

mysql> CREATE USER 'bob'@'localhost' IDENTIFIED BY 'bobpw';
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE USER 'clara'@'localhost' IDENTIFIED BY 'clarapw';
Query OK, 0 rows affected (0.01 sec)
```
3. Set Password Expiry for Alice (password expires after 180 days):
```bash
mysql> ALTER USER 'alice'@'localhost' PASSWORD EXPIRE INTERVAL 180 DAY;
Query OK, 0 rows affected (0.01 sec)
```
4. Verify Alice's Password Settings:
```bash
mysql> SELECT User, password_expired, password_last_changed, password_lifetime, account_locked
    -> FROM mysql.user
    -> WHERE User = 'alice';
```
5. Expected output:
``` bash
+-------+------------------+-----------------------+-------------------+----------------+
| User  | password_expired | password_last_changed | password_lifetime | account_locked |
+-------+------------------+-----------------------+-------------------+----------------+
| alice | N                | 2024-10-16 03:44:39   |               180 | N              |
+-------+------------------+-----------------------+-------------------+----------------+
1 row in set (0.00 sec)
```
### 📝 PART 2: Table Creation and Permissions Setup
1. Create Tables
Create the tables data1, data2, and data3 in the ine_project database:
```bash
USE ine_project;

CREATE TABLE data1 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    column1 VARCHAR(255)
);

CREATE TABLE data2 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    column2 VARCHAR(255)
);

CREATE TABLE data3 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    column3 VARCHAR(255)
);

SHOW TABLES;
```
Expected output:
```bash
+-----------------------+
| Tables_in_ine_project |
+-----------------------+
| data1                 |
| data2                 |
| data3                 |
+-----------------------+
```
2. Grant Permissions to Users
- Alice: Full access to all tables.
```bash
GRANT ALL PRIVILEGES ON ine_project.* TO 'alice'@'localhost';
```
- Bob:
Read-only access to data1:
```bash
GRANT SELECT ON ine_project.data1 TO 'bob'@'localhost';
```
Insert-only access to data2 (can insert rows but not update or delete):
```bash
GRANT INSERT ON ine_project.data2 TO 'bob'@'localhost';
```
Update-only access to data3 (can modify rows but not insert or delete):
```bash
GRANT UPDATE ON ine_project.data3 TO 'bob'@'localhost';
```
- Clara:
Delete-only access on all tables (cannot read or update rows):
```bash
GRANT DELETE ON ine_project.data1 TO 'clara'@'localhost';
GRANT DELETE ON ine_project.data2 TO 'clara'@'localhost';
GRANT DELETE ON ine_project.data3 TO 'clara'@'localhost';
```
Apply changes:
```bash
FLUSH PRIVILEGES;
```

### 📋 Testing User Permissions
- Alice: Should be able to perform all actions (read, insert, update, delete) on all tables.
- Bob:
  1. Can read from data1.
  2. Can insert new rows into data2, but not modify or delete existing rows.
  3. Can update existing rows in data3, but not insert or delete rows.
- Clara: Can only delete rows from all tables but cannot read or modify them.
