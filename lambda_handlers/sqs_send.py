import json
from botocore.exceptions import ClientError
from utility.aws_utils import (
    create_sqs_queue,
    send_message_to_sqs,
    sts_assume_role,
    log_to_cloudwatch
)

# call lambda_handler from UI with selected queries
def lambda_handler(event: dict, context):
    message = json.dumps(event)
    log_to_cloudwatch(
        message=message,
        log_group_name='/aws/lambda/guardian_sqs_send',
        log_stream_name='sqs_send_log_stream',

    )
    params = event['params']['querystring']
    queue_name = params['queue-name'] or 'guardian-queue'
    # query = params['query']
    # opts = [[opt, params[opt]] for opt in params]
    
    send(queue_name, message)


def send(queue_name: str, message: str) -> None:
    """
    Send a message to an SQS queue.

    Args:
        queue_name (str): The name of the SQS queue.
        message (str): The message to send to the SQS queue.

    Returns:
        None
    """
    sqs_client = sts_assume_role().client('sqs', 'eu-west-2')
    def check_queue_exists(queue_name: str) -> bool:
        """Check if the SQS queue exists.

        Parameters:
            queue_name (str): The name of the queue as a string.

        Returns:
            bool: True if the queue exists, False otherwise.
        """
        try:
            sqs_client.get_queue_url(QueueName=f"{queue_name}.fifo")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                return False
            else:
                raise e

    if not check_queue_exists(queue_name):
        queue = create_sqs_queue(queue_name=queue_name, cw=[
            "/aws/lambda/guardian_sqs_send",
            "sqs_send_log_stream"
        ])
        queue_url: str = queue["QueueUrl"]
    else:
        queue_url: str = sqs_client.get_queue_url(QueueName=f"{queue_name}.fifo")
        
    send_message_to_sqs(queue_url, message)

