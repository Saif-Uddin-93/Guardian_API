import json
from utility.aws_utils import create_sqs_queue, send_message_to_sqs, \
    receive_messages_from_sqs
from api_handler.api_utils import get_guardian_data


def test_recieve_messages_from_sqs(sqs_client):
    queue = create_sqs_queue(queue_name = "Test", client = sqs_client)
    queue_url = queue["QueueUrl"]
    message = "Test message."
    send_message_to_sqs(url = queue_url, message = message, client = sqs_client)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client)
    assert queue_messages[0]["Body"] == message


def test_receive_json_from_sqs(sqs_client):
    json_response : str = json.dumps(get_guardian_data("tech"))
    queue = create_sqs_queue(queue_name = "Test", client = sqs_client)
    queue_url = queue["QueueUrl"]
    send_message_to_sqs(url = queue_url, message = json_response, client = sqs_client)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client)
    assert queue_messages[0]["Body"] == json_response