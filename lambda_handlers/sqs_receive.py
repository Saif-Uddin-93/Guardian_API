import json
from botocore.exceptions import ClientError
from utility.aws_utils import (
    receive_messages_from_sqs,
    create_iam_role,
    sqs_client
)


def lambda_handler(event: dict, context):
    """
    AWS Lambda function entry point.

    This function is triggered by an event and context, extracts data from a database,
    and stores the data in an S3 bucket. The bucket name is retrieved from environment variables.

    :param event: The event data passed to the Lambda function (as a dictionary).
    :param context: The runtime information of the Lambda function (e.g., function name, version).
    """
    create_iam_role()
    receive(event["queue_name"])


def receive(queue_name: str) -> dict | None:
    """Returns a JSON string.

    Parameters:
        queue_name (str): The name of the queue as a string.

    Returns:
        dict: Returns the messages in the queue as a dictionary of messages (str)
    """
    def check_queue_exists(queue_name: str) -> bool:
        """Check if the SQS queue exists.

        Parameters:
            queue_name (str): The name of the queue as a string.

        Returns:
            bool: True if the queue exists, False otherwise.
        """
        try:
            sqs_client.get_queue_url(QueueName=queue_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                return False
            else:
                raise e

    if not check_queue_exists(queue_name):
        raise ValueError("Queue does not exist.")
    else:
        queue_url: str = sqs_client.get_queue_url(QueueName=queue_name)
    
    response = json.loads(receive_messages_from_sqs(queue_url))
    return response