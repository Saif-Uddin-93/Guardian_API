#!/usr/bin/env python
import json
from utility.aws_utils import (
    create_sqs_queue,
    receive_messages_from_sqs,
)


def lambda_handler(event: dict, context):
    """
    AWS Lambda function entry point.

    This function is triggered by an event and context, extracts data from a database,
    and stores the data in an S3 bucket. The bucket name is retrieved from environment variables.

    :param event: The event data passed to the Lambda function (as a dictionary).
    :param context: The runtime information of the Lambda function (e.g., function name, version).
    """

    receive(event["queue_name"])


def receive(queue_name: str) -> dict | None:
    """Returns a JSON string.

    Parameters:
        queue_name (str): The name of the queue as a string.

    Returns:
        dict: Returns the messages in the queue as a dictionary of messages (str)
    """
    queue = create_sqs_queue(queue_name)
    queue_url: str = queue["QueueUrl"]
    response: dict = json.loads(receive_messages_from_sqs(queue_url))
    return response
