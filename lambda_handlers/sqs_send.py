import json
from botocore.exceptions import ClientError
from utility.api_utils import get_guardian_data
from utility.aws_utils import (
    create_sqs_queue,
    send_message_to_sqs,
    sqs_client
)

# call lambda_handler from UI with selected queries
def lambda_handler(event: dict, context):
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
        queue = create_sqs_queue(queue_name)
        queue_url: str = queue["QueueUrl"]
    else:
        queue_url: str = sqs_client.get_queue_url(QueueName=queue_name)
        
    send_message_to_sqs(queue_url, message)

