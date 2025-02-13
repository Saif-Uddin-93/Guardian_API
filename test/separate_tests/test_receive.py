import json
from utility.aws_utils import create_sqs_queue, send_message_to_sqs, \
    receive_messages_from_sqs
from api_handler.api_utils import fetch_api, build_api_url, output_to_json_file


def test_recieve_messages_from_sqs(sqs_client):
    queue = create_sqs_queue(queue_name = "Test", client = sqs_client)
    queue_url = queue["QueueUrl"]
    message = "Test message."
    send_message_to_sqs(url = queue_url, message = message, client = sqs_client)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client)
    # print(queue_messages)
    assert queue_messages[0]["Body"] == message


def test_receive_json_from_sqs(sqs_client):
    json_response : str = json.dumps(fetch_api(build_api_url("tech")))
    queue = create_sqs_queue(queue_name = "Test", client = sqs_client)
    queue_url = queue["QueueUrl"]
    send_message_to_sqs(url = queue_url, message = json_response, client = sqs_client)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client)
    assert queue_messages[0]["Body"] == json_response