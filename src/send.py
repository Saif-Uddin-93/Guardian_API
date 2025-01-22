import pika
import json
from guardian_api import fetch_api, build_api_url

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

json_response : json = fetch_api(build_api_url("tech"))

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body = json_response)
print("[x] Sent json")

connection.close()
