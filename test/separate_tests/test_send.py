import pytest
import os
import boto3
from moto import mock_aws
from botocore.exceptions import ClientError, BotoCoreError


def test_send_message_to_sqs(sqs_client):
    # Create a SQS queue
    queue = sqs_client.create_queue(
        QueueName='Test',
        Attributes={
            'DelaySeconds': '60',
            'MessageRetentionPeriod': '259200000' # 3 days
        }
    )
    queue_url = queue["QueueUrl"]
    message = "Test message."
    
    def send_message():
        try:
            response = sqs_client.send_message(
                QueueUrl=queue_url, 
                MessageBody=message
            )
            
            # Check if the message was successfully sent
            if "MessageId" in response:
                print(f"Message sent successfully! MessageId: {response['MessageId']}")
                return response['MessageId']
            else:
                print("Message sending failed: No MessageId returned")
                return None

        except ClientError as e:
            # Handle AWS Client Errors
            print(f"ClientError: {e.response['Error']['Message']}")
            return None

        except BotoCoreError as e:
            # Handle boto3-related errors
            print(f"BotoCoreError: {str(e)}")
            return None

        except Exception as e:
            # Catch any other unexpected exceptions
            print(f"Unexpected error: {str(e)}")
            return None
        
    assert send_message()