import json
from utility.aws_utils import (
    create_sqs_queue,
    send_message_to_sqs,
    receive_messages_from_sqs
)
from utility.api_utils import get_guardian_data


def test_recieve_messages_from_sqs(sqs_client_fixture, cw_logs_client_fixture):
    """
    Test sending and receiving a single message from SQS.

    Args:
        sqs_client_fixture: The boto3 SQS client.
    """
    queue = create_sqs_queue(
        queue_name="Test", 
        log_group_name="test_group",
        log_stream_name="test_stream",
        client=sqs_client_fixture, 
    )
    queue_url = queue["QueueUrl"]
    message = "Test message."
    send_message_to_sqs(url=queue_url, message=message, client=sqs_client_fixture)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client_fixture)
    assert queue_messages[0]["Body"] == message


def test_receive_json_from_sqs(sqs_client_fixture, cw_logs_client_fixture):
    """
    Test sending and receiving a JSON message from SQS.

    Args:
        sqs_client_fixture: The boto3 SQS client.
    """
    json_response: str = json.dumps(get_guardian_data("tech"))
    queue = create_sqs_queue(
        queue_name="Test", 
        log_group_name="test_group",
        log_stream_name="test_stream",
        client=sqs_client_fixture, 
    )
    queue_url = queue["QueueUrl"]
    send_message_to_sqs(url=queue_url, message=json_response, client=sqs_client_fixture)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client_fixture)
    assert queue_messages[0]["Body"] == json_response


def test_receive_multiple_messages_from_sqs(sqs_client_fixture, cw_logs_client_fixture):
    """
    Test sending and receiving multiple messages from SQS.

    Args:
        sqs_client_fixture: The boto3 SQS client.
    """
    queue = create_sqs_queue(
        queue_name="Test", 
        log_group_name="test_group",
        log_stream_name="test_stream",
        client=sqs_client_fixture, 
    )
    queue_url = queue["QueueUrl"]
    messages = ["Message 1", "Message 2", "Message 3"]
    for message in messages:
        send_message_to_sqs(queue_url, message, sqs_client_fixture)
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client_fixture)
    received_messages = [msg["Body"] for msg in queue_messages]
    assert all(msg in received_messages for msg in messages)


def test_receive_no_messages_from_sqs(sqs_client_fixture, cw_logs_client_fixture):
    """
    Test receiving no messages from an empty SQS queue.

    Args:
        sqs_client_fixture: The boto3 SQS client.
    """
    queue = create_sqs_queue(
        queue_name="Test", 
        log_group_name="test_group",
        log_stream_name="test_stream",
        client=sqs_client_fixture, 
    )
    queue_url = queue["QueueUrl"]
    queue_messages = receive_messages_from_sqs(queue_url, sqs_client_fixture)
    assert len(queue_messages) == 0
