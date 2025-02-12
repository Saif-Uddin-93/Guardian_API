import pika, json, os

import pika.delivery_mode
from api_handler.api_utils import fetch_api, build_api_url
from dotenv import load_dotenv

load_dotenv()

rabbit_user = os.getenv("rabbit-user")
rabbit_pass = os.getenv("rabbit-pass")
rabbit_host = os.getenv("rabbit-host")

credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='queue', durable=True, arguments = {
    "x-message-ttl": 259200000,  # TTL in milliseconds (3 days)
})

json_response : json = json.dumps(fetch_api(build_api_url("tech")))

channel.basic_publish(exchange='',
                    routing_key='queue',
                    body = json_response,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.DeliveryMode.Persistent  # Make message persistent
                    ))
print("[x] Sent json")

connection.close()
