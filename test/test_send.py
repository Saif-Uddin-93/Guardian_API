import pytest, os, boto3
# from moto import mock_aws
from botocore.exceptions import ClientError, BotoCoreError
from utility.aws_utils import create_sqs_queue, send_message_to_sqs


def test_send_message_to_sqs(sqs_client):
    # Create a SQS queue
    queue = create_sqs_queue("Test", client=sqs_client)
    queue_url = queue["QueueUrl"]
    message = "Test message."

    result = send_message_to_sqs(queue_url, message, client=sqs_client)

    assert result
 

def test_send_empty_message_to_sqs(sqs_client):
    # Create a SQS queue
    queue = create_sqs_queue("Test", client=sqs_client)
    queue_url = queue["QueueUrl"]
    message = ""

    with pytest.raises(ClientError):
        send_message_to_sqs(queue_url, message, client=sqs_client)


# def test_send_message_to_nonexistent_queue(sqs_client):
#     queue_url = "https://sqs.us-east-1.amazonaws.com/123456789012/NonExistentQueue"
#     message = "Test message."

#     with pytest.raises(ClientError):
#         send_message_to_sqs(queue_url, message, client=sqs_client)


# def test_send_message_to_sqs_with_invalid_client():
#     queue_url = "https://sqs.us-east-1.amazonaws.com/123456789012/Test"
#     message = "Test message."
#     invalid_client = boto3.client("s3")  # Using S3 client instead of SQS client

#     with pytest.raises(BotoCoreError):
#         send_message_to_sqs(queue_url, message, client=invalid_client)
