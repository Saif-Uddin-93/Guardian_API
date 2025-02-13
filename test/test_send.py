import pytest, os, boto3
from moto import mock_aws
from botocore.exceptions import ClientError, BotoCoreError
from utility.aws_utils import create_sqs_queue, send_message_to_sqs


def test_send_message_to_sqs(sqs_client):
    # Create a SQS queue
    queue = create_sqs_queue("Test", client = sqs_client)
    queue_url = queue["QueueUrl"]
    message = "Test message."
    
    result = send_message_to_sqs(queue_url, message, client = sqs_client)
        
    assert result