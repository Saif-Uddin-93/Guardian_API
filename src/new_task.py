import pika, json, os, sys
from dotenv import load_dotenv

load_dotenv()

rabbit_user = os.getenv("rabbit-user")
rabbit_pass = os.getenv("rabbit-pass")
rabbit_host = os.getenv("rabbit-host")

credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='queue',
                      body=message)
print(f" [x] Sent {message}")
