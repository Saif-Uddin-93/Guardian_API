import pytest
from botocore.exceptions import ClientError
from utility.aws_utils import (
    create_sqs_queue, 
    send_message_to_sqs,
    cw_log_stream
)


def test_send_message_to_sqs(sqs_client_fixture, cw_logs_client_fixture):
    queue = create_sqs_queue(
        queue_name="Test", 
        client=sqs_client_fixture, 
        cw=[
            "test_group",
            "test_stream",
            cw_logs_client_fixture
        ]
    )
    queue_url = queue["QueueUrl"]
    message = "Test message."

    result = send_message_to_sqs(queue_url, message, client=sqs_client_fixture)

    assert result
 

def test_send_empty_message_to_sqs(sqs_client_fixture, cw_logs_client_fixture):
    queue = create_sqs_queue(
        queue_name="Test", 
        client=sqs_client_fixture, 
        cw=[
            "test_group",
            "test_stream",
            cw_logs_client_fixture
        ]
    )
    queue_url = queue["QueueUrl"]
    message = ""

    with pytest.raises(ClientError):
        send_message_to_sqs(queue_url, message, client=sqs_client_fixture)


