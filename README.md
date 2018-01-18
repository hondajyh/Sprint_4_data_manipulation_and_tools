## SPRINT #4: Data Manipulation Libraries & Tools
### 01/10/2018

**Author:** Jon Honda

## What I wanted to do:
### Build a CSV importer to SQLite in python using an object relational mapping solution (ORM). Use SQLAlchemy as my ORM.
__*Some specifications:*__
1. Solution shall be ORM based.
2. csv input file shall consist of data belonging to multiple tables.
3. input column header names shall identify database table and field names.
4. Solution shall "know" how to map between input columns and database table-fields
Why?
- An object relational mapping (ORM) solution simplifies reduces/eliminates SQL coding from my code
- Object oriented approach to SQL coding allows for more object oriented python code

## What I actually was able to do:
- Learned rudimentary SQLAlchemy skills.
- Learned how to import a single CSV file using ORM
- Import a single CSV containing columns belonging to multiple tables, as long as underlying tables have a 1:1 relationship between each other
- Learned about implementing lambda functions.

__*Repo Items:*__
- Readme.md: this file!
- Rudimentary SQLAlchemy Skills:
   - SQLA_Rudimentary.py: setting up SQLAlchemy objects, building 1 table, insert into table, query table, update
   - SQLA_2Tbl_m2m.py: setting up 2 tables w/ a many:many relationship between them. inserting into table, and then inserting associated records
   - SQLA_2Tbl_12m.py: setting up 2 tables 2/ a 1:many relationship between them. inserting into table, and then inserting associated records
- Import a single CSV containing columns belonging to one table:
   - ImportCSV_1Table.py: script file containing solution to import csv data. assumes csv column header names match table names
   - 1_table_input.csv: test file containing data we want to import using ImportCSV_1Table.py
- Import a single CSV containing columns belonging to multiple tables. Table relationships limited to 1:1
   - ImportCSV_MultTable.py: script file containing solution to import csv data.
   - 2_table_input.csv: test file containing data belonging to 2 tables. 
