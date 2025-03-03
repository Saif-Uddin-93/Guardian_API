import pika, os, sys
from dotenv import load_dotenv

load_dotenv()

# Get RabbitMQ credentials and host from environment variables
rabbit_user = os.getenv("rabbit-user")
rabbit_pass = os.getenv("rabbit-pass")
rabbit_host = os.getenv("rabbit-host")

# Set up RabbitMQ connection credentials
credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
# Establish a connection to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbit_host, port=5672, virtual_host="/", credentials=credentials
    )
)
channel = connection.channel()

# Create a message from command line arguments or use a default message
message = " ".join(sys.argv[1:]) or "Hello World!"
# Publish the message to the queue
channel.basic_publish(exchange="", routing_key="queue", body=message)
# Print a confirmation message
print(f" [x] Sent {message}")
