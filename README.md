# Mini SQL Database Engine (Python)

A simplified, in-memory **Mini SQL Engine** built in Python for understanding how SQL operations work under the hood.  
It simulates core database functionalities like **SELECT**, **WHERE**, and **COUNT()**, entirely in memory.

---

## Overview

This project demonstrates how basic SQL query processing works which includes **parsing**, **filtering**, **projection**, and **aggregation**  without using external database systems.

It includes:

- A **Storage module** for loading and storing CSV data  
- An **Engine module** for parsing and executing SQL queries  
- A **REPL (Command-Line Interface)** for interactive SQL querying  

---

## Project Structure

project/
│── storage.py  
│── engine.py  
│── repl.py  
│── employees.csv  
│── examples/  
│── README.md  


## How the System Works

### 1. Storage Module

The **Storage** class acts as a mini in-memory database.

Responsibilities:
- Load CSV files  
- Store table names, columns, and rows  
- Provide table data to the Engine  

Internal structure (conceptually):

self.tables = {  
&nbsp;&nbsp;"employees": {  
&nbsp;&nbsp;&nbsp;&nbsp;"columns": ["id", "name", "age", "department", "salary", "country"],  
&nbsp;&nbsp;&nbsp;&nbsp;"rows": [ {row1}, {row2}, ... ]  
&nbsp;&nbsp;}  
}

- Uses `csv.DictReader` to convert CSV rows into dictionaries.  
- All rows are stored as a list of dictionaries.  

If the CSV has 6 rows, `Storage` holds 6 row dictionaries.

---

### 2. Engine Module

The **Engine** is the brain of the system.

Tasks:
- Parse SQL queries  
- Retrieve tables from Storage  
- Filter using `WHERE`  
- Select columns using `SELECT`  
- Perform aggregations like `COUNT()`  

Query execution flow:

User SQL → Engine.parse_query() → Engine.execute() → Storage.get_table() →  
Filtering (WHERE) → Projection (SELECT) → Aggregation → Return results  

Supported SQL:
- `SELECT *`  
- `SELECT col1, col2`  
- `WHERE` with one condition (`=`, `!=`, `>`, `<`, `>=`, `<=`)  
- `COUNT(*)` and `COUNT(column)`  

---

### 3. REPL (Command Line Interface)

The **REPL** is the interactive interface.

It:
- Initializes Storage and Engine  
- Accepts SQL from the user  
- Sends queries to the Engine  
- Formats and prints results  
- Runs in a loop until `exit` or `quit`  

Example interaction:

sql> `SELECT name, age FROM employees WHERE department = 'Engineering';`

Output:

name age  
Alice 30  
Eve 29  

---

## Example CSV Data

`sample.csv`:

product_id,product_name,category,price,stock
101,Laptop,Electronics,1200,15
102,Keyboard,Electronics,45,100
103,Chair,Furniture,85,50
104,Desk,Furniture,150,20
105,Pen,Stationery,1,500
106,Notebook,Stationery,3,300
107,Headphones,Electronics,90,40
 

---

## Example Queries and Outputs

### 1. SELECT *

```
SELECT * FROM sample;
```

### 2. SELECT specific columns

```
SELECT product_id,product_name FROM employees;
```

Output:

product_id  product_name
101         Laptop
102         Keyboard
103         Chair
104         Desk
105         Pen
106         Notebook
107         Headphones
...

### 3. WHERE filtering

```
  SELECT product_id, category  FROM sample  WHERE product_name = 'Chair';    
```

Output:

product_id  category 
103         Furniture 

### 4. COUNT()

```
  SELECT count(*) from sample;    
```

Output:

count  
7  

---

## Internal Working (Simple Explanation)

### How CSV becomes a table

- Python reads the CSV  
- Each line becomes a dictionary: `{column: value}`  
- All dictionaries stored in a list  

### How SELECT works

- If `*`, return all columns  
- Else, build a new list with only selected columns  

### How WHERE works

- Check each row’s value against the condition  
- Keep rows that match  

### How COUNT works

- Count number of rows after filtering  
- If `COUNT(column)`, ignore null/empty values  

---

## How to Run the Project

### Step 1: Place your CSV file(s) into the project folder

project/  
│── sample.csv  
│── repl.py  

### Step 2: Run the REPL

```
python repl.py
```

### Step 3: Enter CSV filename when prompted

Enter CSV filename to load: `sample.csv`

### Step 4: Start typing SQL queries

sql> `SELECT * FROM sample;`  
sql> `SELECT COUNT(*) FROM sample;`  

---

## Features

- In-memory table storage  
- Simple SQL parsing (SELECT, WHERE, COUNT)  
- User-friendly REPL interface  
- Clear error messages  
- Supports multiple CSV files  

---

## Error Handling

The system displays errors like:

- `Error: Table 'abc' does not exist.`  
- `Error: Column 'salaryy' not found in table.`  
- `Execution error: Invalid SQL syntax.`  

---

## File Responsibilities & Imports

### storage.py

- Loads CSV using `csv.DictReader`  
- Stores tables in dictionaries/lists  
- Imported by: `engine.py`, `repl.py`  

### engine.py

- Parses SQL queries  
- Applies WHERE, SELECT, COUNT  
- Returns results in `{columns: [...], rows: [...]}`  
- Uses a `Storage` instance from REPL  

### repl.py

- CLI interface  
- Loads CSVs  
- Passes SQL to Engine  
- Formats and prints results  

---

## examples/ Folder

examples/  
│── people.csv → Example CSV file  
│── products.csv → Example CSV file  
Purpose:
- Provides ready-to-run CSVs  
- Helps instructors quickly test the engine  

---

## System Flow

1. User runs `repl.py`  
2. REPL creates `Storage()` and `Engine(storage)`  
3. CSV is loaded into Storage  
4. User enters SQL query  
5. Engine parses SQL → fetches table → filters → selects columns → aggregates → returns result  
6. REPL prints result  

---

## Conclusion

This Mini SQL Engine helps understand:

- How databases parse queries  
- Filtering and projection logic  
- Aggregation and counting  
- In-memory data storage and retrieval  

