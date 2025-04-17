import pytest
from botocore.exceptions import ClientError
from utility.aws_utils import (
    create_sqs_queue, 
    send_message_to_sqs
)


def test_send_message_to_sqs(sqs_client_fixture, cw_logs_client_fixture):
    queue = create_sqs_queue(
        queue_name="Test", 
        log_group_name="test_group",
        log_stream_name="test_stream",
        client=sqs_client_fixture, 
    )
    queue_url = queue["QueueUrl"]
    message = "Test message."

    result = send_message_to_sqs(queue_url, message, client=sqs_client_fixture)

    assert result
 

def test_send_empty_message_to_sqs(sqs_client_fixture, cw_logs_client_fixture):
    queue = create_sqs_queue(
        queue_name="Test", 
        log_group_name="test_group",
        log_stream_name="test_stream",
        client=sqs_client_fixture, 
    )
    queue_url = queue["QueueUrl"]
    message = ""

    with pytest.raises(ClientError):
        send_message_to_sqs(queue_url, message, client=sqs_client_fixture)


