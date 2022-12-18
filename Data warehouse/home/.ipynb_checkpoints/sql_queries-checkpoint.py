import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

S3LogData = config.get("S3", "LOG_DATA")
S3LogJson = config.get("S3", "LOG_JSONPATH")
S3SongData= config.get("S3", "SONG_DATA")
DWHARN    = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(artist varchar, auth varchar, firstName varchar, gender varchar, \
                                    itemInSession int, lastName varchar, length float, level varchar, location varchar, method varchar, \
                                    page varchar, registration varchar, sessionId int, song varchar, status int, ts timestamp, \
                                    userAgent varchar, userId int);""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(num_songs int, artist_id varchar, artist_latitude float, \
                                    artist_longitude float, artist_location varchar, artist_name varchar, song_id varchar, \
                                    title varchar, duration float, year int);""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(songplay_id int IDENTITY(0,1) PRIMARY KEY, start_time timestamp NOT NULL SORTKEY, \
                                user_id int NOT NULL, level varchar, song_id varchar, artist_id varchar, session_id int, \
                                location varchar, user_agent varchar);""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(user_id int SORTKEY PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, \
                            level varchar);""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(song_id varchar SORTKEY PRIMARY KEY, title varchar NOT NULL, artist_id varchar, year int, \
                                duration decimal NOT NULL);""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(artist_id varchar SORTKEY PRIMARY KEY, name varchar NOT NULL, location varchar, latitude float, \
                                longitude float);""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(start_time timestamp SORTKEY PRIMARY KEY, hour int, day int, week int, \
                                month int, year int, weekday int);""")

# STAGING TABLES

staging_events_copy = ("""COPY staging_events from {} \
                            region 'us-west-2' timeformat as 'epochmillisecs' iam_role '{}' \
                            format as json {}""").format(S3LogData, DWHARN, S3LogJson)

staging_songs_copy = ("""COPY staging_events from {} \
                            region 'us-west-2' iam_role '{}' \
                            format as json 'auto' """).format(S3SongData, DWHARN)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) \
                            SELECT DISTINCT(se.ts) as start_time, se.userId as user_id, se.level as level, ss.song_id as song_id, ss.artist_id as artist_id, se.sessionId as session_id, se.location as location, se.userAgent as user_agent FROM staging_events se \
                            JOIN staging_songs ss ON se.song = ss.title AND se.artist = ss.artist_name WHERE se.page = 'NextSong'""")

user_table_insert = ("""INSERT INTO users(user_id, first_name, last_name, gender, level) \
                        SELECT DISTINCT(userId) as user_id, firstName as first_name, lastName as last_name, gender, level FROM staging_events WHERE page = 'NextSong' and user_id IS NOT NULL;""")

song_table_insert = ("""INSERT INTO songs(song_id, title, artist_id, year, duration) \
                        SELECT DISTINCT(song_id) as song_id, title, artist_id, year, duration FROM staging_songs WHERE song_id IS NOT NULL;""")

artist_table_insert = ("""INSERT INTO artists(artist_id, name, location, latitude, longitude) \
                            SELECT DISTINCT(artist_id) as artist_id, artist_name as name, artist_location as location, artist_latitude as latitude, artist_longitude as longitude FROM staging_songs WHERE artist_id IS NOT NULL;""")

time_table_insert = ("""INSERT INTO time(start_time, hour, day, week, month, year, weekday) \
                            SELECT DISTINCT(start_time) as start_time, \
                            EXTRACT(hour from start_time) as hour, EXTRACT(day from start_time) as day, EXTRACT(week from start_time) as week, \
                            EXTRACT(month from start_time) as month, EXTRACT(year from start_time) as year, EXTRACT(weekday from start_time) as weekday FROM songplays;""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
