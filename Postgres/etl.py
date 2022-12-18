import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function is used to read the data from the data directory(song file) and insert data into the respective table.
    The data is in JSON format.
    -- Parameters:
        cur: This is the cursor of the database.
        filepath: Path to which the data directory(song file) is located from where the files are taken to analyze.
    -- song_data: takes the values from first file, converts to list and then inserts into the song table.
    -- artist_data: takes the values from first file, converts to list and then inserts into the artist table.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function is used to read the data from the data directory(log file) and insert data into the respective table.
    The data is in JSON format.
    -- Parameters:
        cur: This is the cursor of the database.
        filepath: Path to which the data directory(log file) is located from where the files are taken to analyze.
    -- Filter the file where page is NextSong and then convert the timestamp column into datetime from where we extract data
       as needed format and specify
       labels to the values.
    -- Finally creating a dataframe to combine labels and values from a dictionary and inserting data into the time table.
    -- Insert needed data into the users table.
    -- Extract and insert data into the songplays table.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit = 'ms')

    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit = 'ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function is used to read the data from the data directory(log file) and insert data into the respective table.
    The data is in JSON format.
    -- Parameters:
        cur: This is the cursor of the database.
        filepath: Path to which the data directory is located from where the files are taken to analyze.
        conn: Establish connection to the database.
        func: Function to process song or log file.
    -- Returns:
        Files processed.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Establish a connection with the database and provides a cursor.
    Performs the data extraction and loading to the database.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()