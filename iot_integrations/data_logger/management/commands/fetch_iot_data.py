import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
import csv
import time
import os
from django.conf import settings

# Get the root directory path using BASE_DIR
root_dir = settings.BASE_DIR

# Define the relative path to the CSV file
csv_file_path = os.path.join(root_dir, 'csv', 'room_iot_data.csv')

class Command(BaseCommand):
    help = 'Publish IoT data from a CSV file to MQTT'

    def handle(self, *args, **kwargs):
        # This is the Publisher
        client = mqtt.Client()
        client.connect("test.mosquitto.org", 1883, 60)

        # Open and read the CSV file
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Construct the message from all fields in the CSV row
                message = f"datetime: {row['datetime']}, device_id: {row['device_id']}, datapoint: {row['datapoint']}, value: {row['value']}"
                client.publish("topic/test", message)
                print("Message published: ", message)
                time.sleep(5)  # Wait for 5 seconds before sending the next message

        client.disconnect()
        self.stdout.write(self.style.SUCCESS('Messages published from CSV file.'))
