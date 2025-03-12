import json
from typing import Any
from utility.api_utils import fetch_api, build_api_url
from utility.aws_utils import create_sqs_queue, send_message_to_sqs, sqs_client


# call lambda_handler from UI with selected queries
def lambda_handler(event: dict, context: Any):
    """
    AWS Lambda function entry point.

    This function is triggered by an event and context, extracts data from a database,
    and stores the data in an S3 bucket. The bucket name is retrieved from environment variables.

    :param event: The event data passed to the Lambda function (as a dictionary).
    :param context: The runtime information of the Lambda function (e.g., function name, version).
    """
    query_params = event.get('queryStringParameters', {})
    name = query_params.get('name', 'unknown')
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Hello, {name}!"})
    }


def send(queue_name: str, message: str) -> None:
    """
    Send a message to an SQS queue.

    Args:
        queue_name (str): The name of the SQS queue.
        message (str): The message to send to the SQS queue.

    Returns:
        None
    """
    if type(queue_name) != str or type(message) != str:
        raise TypeError("inputs must be a string")
    queue = create_sqs_queue(queue_name)
    queue_url: str = queue["QueueUrl"]
    send_message_to_sqs(queue_url, message)
