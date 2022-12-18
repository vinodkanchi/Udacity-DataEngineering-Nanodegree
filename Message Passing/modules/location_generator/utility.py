import json
import logging
import os

from kafka import KafkaProducer
from typing import Dict

TOPIC_NAME = "location-data" # os.environ["TOPIC_NAME"]
KAFKA_SERVER = "udaconnect-kafka-0.udaconnect-kafka-headless.default.svc.cluster.local:9092" #os.environ["KAFKA_SERVER"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-generator-service")

# Create the kafka producer
producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])


def publish_location(location_data):
    print(f"Data to be sent to kafka: {location_data}")
    encoded_data = json.dumps(location_data).encode('utf-8')
    print(f"Data to be sent to kafka: {encoded_data}")
    producer.send(TOPIC_NAME, encoded_data)
    producer.flush()

    logger.info(f"Location {location_data} is generated and written to kafka successfully.")






