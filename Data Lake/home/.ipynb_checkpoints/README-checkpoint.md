# Project: Data Lake

## Introduction
A music streaming app, Sparkify has grown their user base and wants to move to data lake.

Data is in S3. We build ETL pipeline that extracts data from data lake on S3, process using Spark.

Deploy in EMR cluster of AWS and load back to parquet format.

## Project Datasets:
The project contains two datasets. These data are in JSON format. They are:

1. Song data in s3://udacity-dend/song_data
The song data consists of song and artist details.

2. Log data in s3://udacity-dend/log_data
The log data logs data from a music streaming app.

## Tables:
### Fact table:

**songplays**:  records in log data associated with song plays
    Contains: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables:

1. **users** - users in the app
    user_id, first_name, last_name, gender, level

2. **songs** - songs in music database
    song_id, title, artist_id, year, duration

3. **artists** - artists in music database
    artist_id, name, location, lattitude, longitude

4. **time** - timestamps of records in songplays
    start_time, hour, day, week, month, year, weekday

## ETL Pipeline

1. Load credentials

2. Read data from S3

3. Process data using Spark through the five tables.

4. Load back to S3 using the parquet.

## Run

1. Create a dl.cfg file with your credentials.
    KEY and SECRET.

2. Create S3 bucket where output results will be stored.

3. Run etl.py
    python etl.py

