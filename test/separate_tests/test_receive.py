from utility.aws_utils import create_sqs_queue, send_message_to_sqs, receive_messages_from_sqs


# def test_connect_to_rabbitmq_server():
#     pass

def test_recieve_messages_from_sqs(sqs_client):
    queue = create_sqs_queue(queue_name = "Test", client = sqs_client)
    queue_url = queue["QueueUrl"]
    message = "Test message."
    send_message_to_sqs(url = queue_url, message = message, client = sqs_client)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client)
    print(queue_messages)
    assert queue_messages["Messages"][0]["Body"] == message