import os
from kafka import KafkaConsumer
from utility import save_location

TOPIC_NAME = "location-data" #os.environ["TOPIC_NAME"]
KAFKA_SERVER = "udaconnect-kafka-0.udaconnect-kafka-headless.default.svc.cluster.local:9092" # os.environ["KAFKA_SERVER"]

# Create the kafka consumer
passing = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])

while True:
    for message in passing:
        location_data = message.value.decode('utf-8')
        save_location(location_data)
