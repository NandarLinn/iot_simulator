# IoT Simulator Django Application
## Introduction

This document outlines the design and functionality of the "iot_simulator" Django application, particularly focusing on the "data_logger" app. The application is designed to manage and record IoT data within a hotel environment.

### Data Model
####  ER Diagram
![Alt](https://github.com/NandarLinn/iot_simulator/blob/main/demo_images/1.png)

#### Hotel Model
  - name: This CharField represents the name of the hotel.
  - The Hotel model represents a hotel entity, primarily identified by its name.

#### Floor Model
  - hotel: This ForeignKey establishes a many-to-one relationship with the Hotel model, linking each floor to a specific hotel.
  - number: This IntegerField represents the floor number within the hotel.
    The Floor model represents individual floors within a hotel, associating each floor with a specific hotel and assigning a unique floor number.
#### Room Model
  - floor: This ForeignKey establishes a many-to-one relationship with the Floor model, linking each room to a specific floor.
  - number: This CharField (max length: 10) represents the room number or identifier.
    The Room model represents individual rooms within a floor, associated with a specific floor, and assigned a unique room number.

#### IoTData Model
  - room: This ForeignKey establishes a many-to-one relationship with the Room model, linking each IoT data entry to a specific room.
  - datetime: This DateTimeField stores the date and time when the data was recorded.
  - device_id: This CharField (max length: 20) represents the device's unique identifier.
  - datapoint: This CharField (max length: 20) specifies the type or category of the recorded data.
  - value: This CharField (max length: 20) stores the actual value of the recorded data.
    The IoTData model represents data collected from IoT devices installed in individual rooms. Each data entry is associated with a specific room and includes information about the date and time of recording, the device's ID, the data point category, and the recorded value.

To review the table schema, kindly refer to the [Model](https://github.com/NandarLinn/iot_simulator/blob/main/iot_integrations/data_logger/models.py) file.

### Database Setup

Django's Object-Relational Mapping (ORM) will create the necessary database tables based on the defined models. Use the following commands to generate and apply database migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```
This will create the database tables required to store hotel, floor, room, and IoT data.

### Data Import

You can populate the database with hotel-related data either via the Django admin panel or by using CSV data. Use the following script to import data from a CSV file:
```sh
python manage.py import_hotel_floor_room_data /your_hotel_floor_room_data.csv
```
This script allows you to conveniently import data into the application.
This will start the development server, making the application accessible via a web browser.
Kindly refer to the [import_hotel_floor_room.py](https://github.com/NandarLinn/iot_simulator/blob/main/iot_integrations/data_logger/management/commands/import_hotel_floor_room.py) file.

### API Endpoints

The application provides the following API endpoints for data retrieval:
```sh
/hotels/: Retrieve all hotels.
/hotels/<hotel_id>/floors/: Access floors in a specific hotel.
/floors/<floor_id>/rooms/: List rooms on a particular floor.
/rooms/<room_id>/data/: Get IoT data for a specific room.
/rooms/<room_id>/data/life_being/: Retrieve Life Being sensor data for a room.
/rooms/<room_id>/data/iaq/: Retrieve Indoor Air Quality (IAQ) sensor data for a room.
```

These endpoints allow users to interact with the data stored in the application through HTTP requests.

### Subscribe IoTData

A Python script is provided to subscribe to MQTT data from a specified topic and store it in the Django database. The script uses the Paho MQTT client library to connect to an MQTT broker, receive messages, parse them into key-value pairs, and save relevant data to the IoTData model in the database.

To execute the MQTT Subscriber script, use the following command:
```sh
python manage.py subscribe_iot_data
```
Kindly refer to the [subscribe_iot_data.py](https://github.com/NandarLinn/iot_simulator/blob/main/iot_integrations/data_logger/management/commands/subscribe_iot_data.py) file.
This script is intended for use within a Django project where real-time IoT data needs to be captured and logged in a database.

![Alt](https://github.com/NandarLinn/iot_simulator/blob/main/demo_images/2.png)



### MQTT Publisher

Another Python script is provided to publish IoT data from a CSV file to an MQTT broker. Ensure that the CSV file is located in the csv directory of your Django project. Before running the script, configure the MQTT broker by modifying the client.connect line within the handle function. By default, it connects to the public MQTT broker test.mosquitto.org on port 1883.

To execute the MQTT Publisher script, use the following command:
```sh
python manage.py fetch_iot_data
```
Kindly refer to the [fetch_iot_data.py](https://github.com/NandarLinn/iot_simulator/blob/main/iot_integrations/data_logger/management/commands/fetch_iot_data.py) file.

![Alt](https://github.com/NandarLinn/iot_simulator/blob/main/demo_images/3.png)

## Building chat bot using openai, langchain and gradio interface
The current database is connected to Langchain, a tool known as large language models (LLMs), that helps connect advanced language software, with other sources of information, like databases. But there has limitation for free api key.
Important: To test chatbot api replace with your openai key because personal use for openai key is disable when repo is public to github as I bought API key for personal use.
```sh
OPENAI_KEY = YOUR-OPENAI-KEY
```

```sh
def handle(self, *args, **options):
        DB_URI = 'sqlite:///db.sqlite3'
        OPENAI_KEY = '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'
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.ClearButton([msg, chatbot])
            def respond(message, chat_history):
                llm = OpenAI(temperature=0, openai_api_key=OPENAI_KEY)
                db_uri = DB_URI
                db = SQLDatabase.from_uri(db_uri)
                db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
                bot_message = db_chain.run(message)
                chat_history.append((message, bot_message))
                time.sleep(2)
                return "", chat_history
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
        demo.launch()
```
To execute the API, use the following command:
```sh
python management.py chatbot
```
## Run iot_simulator app and chatbot using docker
```sh
docker-compose up --build --force-recreate
```
To execute the server, use the following command:

- For iot_simulator:
  ```sh
  http://0.0.0.0:8000/api
  ```
![Alt](https://github.com/NandarLinn/iot_simulator/blob/main/demo_images/djangoserver.gif)

- For chatbot:
  ```sh
  http://0.0.0.0:7860
  ```
![Alt](https://github.com/NandarLinn/iot_simulator/blob/main/demo_images/4.png)

## Conclusion

The "iot_simulator" Django application is a powerful tool for managing IoT data within a hotel environment. It provides a comprehensive database structure, API endpoints for data retrieval, and MQTT integration for real-time data handling. It offers flexibility and ease of use for managing and analyzing IoT data in a hotel setting.


## Future Works
- Create Stable Data Models
- To integrate with cloud centralized database.
## Send a maid/food request to the hotel staff
### Transferring Guest Requests to the Correct Department:
#### User Interface for Guests:
  - Guests should have a user-friendly interface, such as a mobile app or web portal, to submit their requests. Each request should have a category (maid or food) and additional details.
#### Request Routing:
- Categorize incoming requests based on the type (maid or food). You can use a form with a dropdown menu for guests to select the request type.
- Use Django forms to validate and process guest requests.
#### Routing Logic:
  - Implement a routing logic within the application to determine the correct department based on the request type. For example:
  - For cleaning tasks (maid requests), route requests to the "Maid Department."
  - For ordering food, route requests to the "Kitchen Department."
#### Internal Notifications:
  Integrate a notification system that automatically notifies the respective department when a request is received. You can use messaging systems like email or real-time messaging services.

### Method for Hotel Staff to Notice and Acknowledge Requests:
#### Internal Dashboard:
  - Create an internal dashboard or notification system for hotel staff. This dashboard can display incoming guest requests along with relevant details and categories (maid or food).
#### Assignment and Acknowledgment:
  - Hotel staff can view requests in the dashboard and acknowledge them. Once a request is acknowledged, it's marked as in progress.
#### Status Updates:
  - Implement a status update mechanism for requests. Staff can update the status (e.g., "acknowledged," "in progress," "completed") to keep track of the request's progress.

### Method for Guests to Track Request Progress:
#### Guest Portal:
  - Provide guests with a portal where they can track the progress and status of their requests. This portal can be part of the mobile app or website.
#### Real-Time Updates:
  - Enable real-time updates for the guest portal. Whenever there's a change in the request's status (e.g., the maid has started cleaning, or food is on the way), the guest should receive immediate updates.
#### Status Codes:
  Use status codes to clearly indicate the request's progress. For example, "Acknowledged," "In Progress," "Completed," or "Cancelled."
#### Messaging Feature:
  - Implement a messaging feature that allows guests to communicate with hotel staff regarding their requests. This can be particularly useful if there are delays or additional details needed.
#### Confirmation and Feedback:
  - Once the request is completed, allow guests to confirm that their request was fulfilled and provide feedback. This helps in maintaining the quality of service.

## User Role and Authorization
### Define User Roles:
### Guest:
  - Guests are unauthenticated or partially authenticated users.
  - They have limited access, typically to public pages, such as viewing hotel information and rooms.
#### Registered User:
  - Registered users have created an account and logged in.
  - They can access personalized features, such as submitting requests or making reservations.
#### Staff:
  - Staff members include hotel employees like maids, kitchen staff, and front desk personnel.
  - They have specific job-related permissions, such as handling guest requests and managing room availability.
  - Staff members should be assigned to different departments (maid, kitchen, etc.), and their permissions should align with their roles.
#### Admin:
  - Admin users have the highest level of access and control over the application.
  - They can manage user accounts, define user roles and permissions, and access the admin dashboard.

## Role-Based Authorization:
#### Use Django's Built-in User Model:
  - Utilize Django's built-in User model for user authentication.
  - Create custom user profiles to extend the user model with additional information and fields specific to each role.
#### Permissions and Access Levels:
  - Define permissions for each role. Django's built-in Permissions system can be used for this purpose.
  - For example, a staff member might have permissions to update room availability, while an admin has permissions to create and delete user accounts.
