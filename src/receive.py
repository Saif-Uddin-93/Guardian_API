#!/usr/bin/env python
import pika, sys, os
import json
from guardian_api import output_to_json_file

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        json_body = json.dumps(body)
        print(f" [x] Received {json_body}")
        output_to_json_file(body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

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