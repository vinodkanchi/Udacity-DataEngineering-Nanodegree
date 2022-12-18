import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth
from pyspark.sql.functions import hour, weekofyear, date_format
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import StructType as R
from pyspark.sql.types import StructField as Fld, DoubleType as Dbl
from pyspark.sql.types import StringType as Str
from pyspark.sql.types IntegerType as Int, DataType as Dat, TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get('AWS', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('AWS', 'AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    """
    Creates/modifies spark session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Loads song data from AWS S3 and processes it.
    Sends the extracted data back into S3
    param spark: Used as a spark session object
    param input_data: AWS S3 location of the data
    param output_data: AWS S3 location where data will be stored.
    """
    # get filepath to song data file
    song_data = input_data + "song_data/*/*/*/*.json"
    
    songSchema = R([
        Fld("artist_id", Str()),
        Fld("artist_latitude", Dbl()),
        Fld("artist_location", Str()),
        Fld("artist_longitude", Dbl()),
        Fld("artist_name", Str()),
        Fld("duration", Dbl()),
        Fld("num_songs", Int()),
        Fld("title", Str()),
        Fld("year", Int()),
    ])
    # read song data file
    df = spark.read.json(song_data, schema=songSchema).dropDuplicates()

    # extract columns to create songs table
    songs_list = ["title", "artist_id", "year", "duration"]
    songs_table = df.select(songs_list).dropDuplicates() \
                    .withColumn("song_id", monotonically_increasing_id())
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(output_data + "songs/", \
                              mode="overwrite", partitionBy=["year", "artist_id"])

    # extract columns to create artists table
    artists_list = ["artist_id", "artist_name", "artist_location", \
                        "artist_latitude", "artist_longitude"]
    artists_table = df.selectExpr(artists_list).dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + "artists/", mode="overwrite")


def process_log_data(spark, input_data, output_data):
    """
    Loads song data from AWS S3 and processes it.
    Sends the extracted data back into S3
    param spark: Used as a spark session object
    param input_data: AWS S3 location of the data
    param output_data: AWS S3 location where data will be stored.
    """
    # get filepath to log data file
    log_data = input_data + "log_data/*/*/*/*.json"

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table
    users_list = ["userId", "firstName", "lastName", "gender", "level"]
    users_table = df.select(users_list).dropDuplicates()
    
    # write users table to parquet files
    users_table.write.parquet(output_data + "users/", mode="overwrite")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x : datetime.fromtimestamp(x / 1000), \
                        TimestampType())
    df = df.withColumn("timestamp", get_timestamp("ts"))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x : to_date(x), TimestampType())
    df = df.withColumn("start_time", get_timestamp("ts"))
    
    # extract columns to create time table
    time_table = df.withColumn("hour", hour("start_time")) \
                  .withColumn("day", dayofmonth("start_time")) \
                  .withColumn("week", weekofyear("start_time")) \
                  .withColumn("month", month("start_time")) \
                  .withColumn("year", year("start_time")) \
                  .withColumn("weekday", dayofweek("start_time")) \
                  .select("start_time", "hour", "day", "week", "month", \
                              "year", "weekday").drop_duplicates()
    
    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(output_data + "time_table/", mode="overwrite", \
                             partitionBy=["year", "month"])

    # read in song data to use for songplays table
    song_df = spark.read.format("parquet").option("basePath", output_data + "songs/") \
                                .load(output_data + "songs/*/*")

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = df.join(song_df, df.song == song_df.title, how="inner") \
                  .select(monotonically_increasing_id().alias("songplay_id"), \
                         col("start_time"), col("start_time"), \
                         col("userId").alias("user_id"), \
                         col("level"), col("song_id"), col("artist_id"), \
                         col("sessionId").alias("session_id"), \
                         col("location"), col("userAgent").alias("user_agent"))
                  
    songplays_table = songplays_table.join(time_table, \
                                songplays_table.start_time == time_table.start_time, \
                                how="inner").select("songplay_id", \
                                songplays_table.start_time, "user_id", \
                                "level", "song_id", "artist_id", \
                                "session_id", "location", "user_agent", "year", "month") \
                                .drop_duplicates()

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.parquet(output_data + "songplays/", mode="overwrite", \
                                      partitionBy=["year", "month"])


def main():
    """
    Main function to run the entire program
    """
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://sparkify-data-udend/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
