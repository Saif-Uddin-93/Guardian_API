import json
from utility.api_utils import get_guardian_data
from utility.aws_utils import create_sqs_queue, send_message_to_sqs

# call lambda_handler from UI with selected queries
def lambda_handler(event, context):
    # Get query string parameters directly from event
    params = event['params']['querystring']
    query = params['query']
    queue_name = params['queue-name']
    opts = [[opt, params[opt]] for opt in params]
    data = get_guardian_data(query, opts)
    
    send(queue_name, json.dumps(data))

    return {
        'statusCode': 200,
        'guardian': data
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

