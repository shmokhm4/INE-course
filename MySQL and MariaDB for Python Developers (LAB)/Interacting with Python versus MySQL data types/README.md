# 5th Lab in the Course:Interacting with Python versus MySQL Data Types 💫
In this project, you will explore the interfaces between Python data types and MySQL data types. The aim is to understand how different Python collections (such as namedtuples, dictionaries, and lists) can be mapped to appropriate MySQL data types, and how to infer database schemas from these collections.

## Features ✨

- **Data Type Unification**: The `unify_datatype()` function determines the appropriate MySQL data type for various Python values, including floats, integers, decimals, strings (such as currency), and fractions.
  
- **Schema Inference**: The `infer_schema_iterable()` function infers SQL schemas from different iterable collections. It can handle:
  - Namedtuples
  - Dictionaries
  - Lists and Tuples
  - Custom Python objects

- **NULL Handling**: The project accounts for potential NULL values in the data, determining which columns may be nullable based on the presence of `None` in the datasets.

- **Flexible Input**: The code is designed to work with heterogeneous collections, making it adaptable for various data sources.

## Sample output 🪄
```bash
CREATE TABLE Numbers1 (
    a DOUBLE PRECISION,
    b DECIMAL(26, 25),
    c BIGINT,
    d SMALLINT,
    e DOUBLE PRECISION
);
--------------------------------------------------
CREATE TABLE Numbers1 (
    a DOUBLE PRECISION,
    b DECIMAL(26, 25),
    c BIGINT,
    d SMALLINT,
    e DOUBLE PRECISION
);
--------------------------------------------------
CREATE TABLE Numbers3 (
    a DECIMAL(10, 2),
    b DECIMAL(26, 25),
    c BIGINT,
    d SMALLINT,
    e DOUBLE PRECISION
);
--------------------------------------------------
CREATE TABLE tuple (
    col0 DECIMAL(10, 2),
    col1 DECIMAL(26, 25),
    col2 BIGINT,
    col3 SMALLINT,
    col4 DOUBLE PRECISION
);
--------------------------------------------------
CREATE TABLE Numbers1 (
    a DECIMAL(10, 2),
    b DECIMAL(26, 25),
    c SMALLINT,
    d SMALLINT,
    e DOUBLE PRECISION
);
--------------------------------------------------
CREATE TABLE Numbers1 (
    a DOUBLE PRECISION,
    b DECIMAL(26, 25),
    c DECIMAL(21),
    d SMALLINT,
    e DOUBLE PRECISION
);
--------------------------------------------------
```
