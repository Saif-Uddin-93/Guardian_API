#!/usr/bin/env python
import json, sys
from typing import Any
from api_handler.api_utils import get_guardian_data
from utility.aws_utils import (
    create_sqs_queue,
    receive_messages_from_sqs,
    sqs_client,
    s3_client,
)
from datetime import datetime as dt


def lambda_handler(event: dict, context: Any):
    """
    AWS Lambda function entry point.

    This function is triggered by an event and context, extracts data from a database,
    and stores the data in an S3 bucket. The bucket name is retrieved from environment variables.

    :param event: The event data passed to the Lambda function (as a dictionary).
    :param context: The runtime information of the Lambda function (e.g., function name, version).
    """
    # try:
    # timestamp = str(int(dt.timestamp(dt.now())))
    # key = f"quote_{timestamp}.json"
    # write_result = write_to_s3(s3_client, output_data, BUCKET_NAME, key)
    # if write_result:
    #     logger.info("Wrote quotes to S3")
    # else:
    #     logger.info("There was a problem. Quotes not written.")
    # except Exception as e:
    #     logger.info(f"Unexpected Exception: {str(e)}")
    queue = " ".join(sys.argv[1:]) or "queue"
    receive(queue)


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
