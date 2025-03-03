import pika, json, os

import pika.delivery_mode
from api_handler.api_utils import fetch_api, build_api_url
from dotenv import load_dotenv

load_dotenv()

# Get RabbitMQ credentials and host from environment variables
rabbit_user = os.getenv("rabbit-user")
rabbit_pass = os.getenv("rabbit-pass")
rabbit_host = os.getenv("rabbit-host")

# Set up RabbitMQ connection credentials
credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
# Establish a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

# Declare a queue with a TTL (time-to-live) of 3 days
channel.queue_declare(queue='queue', durable=True, arguments = {
    "x-message-ttl": 259200000,  # TTL in milliseconds (3 days)
})

# Fetch data from The Guardian API and convert it to JSON format
search_query="tech"
json_response : json = json.dumps(fetch_api(build_api_url(search_query)))

# Publish the JSON response to the queue with persistent delivery mode
channel.basic_publish(exchange='',
                    routing_key='queue',
                    body = json_response,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.DeliveryMode.Persistent  # Make message persistent
                    ))
# Print a confirmation message
print("[x] Sent json")

connection.close()
