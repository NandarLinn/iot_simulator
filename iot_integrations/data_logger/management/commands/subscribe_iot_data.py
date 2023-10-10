import paho.mqtt.client as mqtt
import re
from django.core.management.base import BaseCommand
from data_logger.models import IoTData  # Replace 'yourapp' with the actual name of your Django app
from datetime import datetime, timezone
import random

class Command(BaseCommand):
    help = 'Subscribe to MQTT data and store it in the database'

    def handle(self, *args, **kwargs):
        # Callback function when the client connects to the MQTT broker
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")
            # Subscribe to the MQTT topic where data is published
            client.subscribe("topic/test")

        # Callback function when a message is received from the MQTT broker
        def on_message(client, userdata, msg):
            print(f"Received message: {msg.payload.decode()}")

            # Parse the data as key-value pairs
            key_value_pairs = msg.payload.decode().split(',')

            # Initialize an empty dictionary
            data_dict = {}

            # Iterate through key-value pairs and build the dictionary
            for pair in key_value_pairs:
                key, value = pair.split(': ', 1)
                key = key.strip().lower()  # Convert key to lowercase for consistency
                # Remove double quotes from the value, if present
                value = value.strip('"')
                data_dict[key] = value

            print('data_dict: ', data_dict)
            # Extract values from the dictionary
            datetime_str = data_dict.get('datetime')
            device_id = data_dict.get('device_id')
            datapoint = data_dict.get('datapoint')
            value = data_dict.get('value')
            print('datetime_str: ', datetime_str)
            print('device_name: ', device_id)
            print('datapoint: ', datapoint)
            print('value: ', value)

            # Convert datetime string to a datetime object
            if datetime_str:
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc)
                print('datetime_obj: ', datetime_obj)
            else:
                print('datetime field not found in the MQTT message.')

            # Check if required values are not None
            if datetime_obj is not None and device_id is not None and datapoint is not None:
                room_id = random.randint(1, 90)
                mqtt_data = IoTData(
                    room_id=room_id,
                    datetime=datetime_obj,
                    device_id=device_id,
                    datapoint=datapoint,
                    value=value
                )
                mqtt_data.save()
                print("Data saved to the database.")
            else:
                print("Received data is missing required information.")

        # Create an MQTT client
        client = mqtt.Client()

        # Set up the callback functions
        client.on_connect = on_connect
        client.on_message = on_message

        # Connect to the MQTT broker
        client.connect("test.mosquitto.org", 1883, 60)

        # Start the MQTT client's loop to listen for messages
        client.loop_forever()
