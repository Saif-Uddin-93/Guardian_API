import pika, json, os
from guardian_api import fetch_api, build_api_url
from dotenv import load_dotenv

load_dotenv()

rabbit_user = os.getenv("rabbit-user")
rabbit_pass = os.getenv("rabbit-pass")

credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='fileserver', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='queue')

json_response : json = fetch_api(build_api_url("tech"))

channel.basic_publish(exchange='',
                      routing_key='queue',
                      body = json_response)
print("[x] Sent json")

connection.close()
