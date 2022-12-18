# Data Modelling with Postgres

The project aims at initiating work at a startup called Sparkify.

This startup wants to process and anlayze the data, they have been collecting.

The data that they tend to collect are songs and user activity which is on their app.

The data is available in JSON format and this data has to be used forward to the analysis.

We create a database using the SQL database Postgres and create necessary tables as per requirement.

Later the tables and ETL piplelines are created and has to be tested for the data that has been available.

# Database Schema:

1. Fact Table: **songplays** (stores record in log data in respect to record of the songs)
columns: 
-songplay_id(Primary key)
-start_time, 
-user_id
-level
-song_id
-artist_id
-session_id
-location
-useragent
    
2. Dimension Tables:

a. **users** :(stores record of users in app)
columns: 
-user_id(Primary key)
-first_name
-last_name
-gender
-level

b. **songs** :(stores songs/music list in app)
columns: 
-song_id(Primary key)
-title
-artist_id
-year
-duration

c. **artists** :(stores artists record in app)
columns: 
-artist_id(Primary key)
-name
-location
-latitute
-longitute

d. **time** :(stores timestamp in app)
columns: 
-start_time(Primary key)
-hour
-day
-week
-month
-year
-weekday

# ETL:
1. **sql_queries** : query statements to run different functions as shown below:
creating and droping a table, inserting data into the table and selecting a particular data from the table.

2. **create_tables** : runs the sql_queries and does the function in the queries.

3. **etl** : process the data from the directory and inserts the data into the tables.
    
# Program Run:

1. Create the SQL queries in sql_queries.py and run the create_table.py using **python3 create_tables.py**

2. To load data into the table, complete the etl.ipynb, etl.py and run **python3 etl.py**

3. To check if all the conditions are satisfied, run **test.ipynb** cell by cell.



