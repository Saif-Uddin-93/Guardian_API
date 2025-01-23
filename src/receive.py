#!/usr/bin/env python
import pika, sys, os, json
from guardian_api import output_to_json_file
from dotenv import load_dotenv

load_dotenv()

rabbit_user = os.getenv("rabbit-user")
rabbit_pass = os.getenv("rabbit-pass")

def main():
    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='fileserver', port=5672, virtual_host='/', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='queue')

    def callback(ch, method, properties, body):
        json_body = json.dumps(body)
        print(f" [x] Received {json_body}")
        output_to_json_file(body)

    channel.basic_consume(queue='queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt:
        print('\nInterrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)