# Project Data Warehouse

A startup Sparkify tends to move its data to cloud. It has data currently in S3 buckets.

The data is in the form of JSON. The data are user log and songs.

We build an ETL pipeline, that takes data from S3 and stages in Redshift and transform them into tabular data.

# Database Design

Data stored in S3 bucket is extracted to two tables namely: **staging_events** and **staging_songs** on Redshift.

The data is then transformed into the schema consisting fact and dimension tables.

### Fact Table

**songplays** : songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables

**users** :user_id, first_name, last_name, gender, level

**songs** :song_id, title, artist_id, year, duration

**artists** : artist_id, name, location, lattitude, longitude

**time** : start_time, hour, day, week, month, year, weekday

# Project Run:

1. Give the necessary credentials to the **dwh.cfg** file.

2. Fill in the **sql_queries.py** to create tables, extract and insert data into the tables.

3. Run the **create_tables.py** to create the necessary action related to table creation.

4. Run the **etl.py** file to load the data into the tables.

