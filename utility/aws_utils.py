import boto3, os, json
from botocore.exceptions import ClientError, BotoCoreError
from dotenv import load_dotenv

load_dotenv()

region_name = "eu-west-2"

# sqs client
sqs_client = boto3.client('sqs')

def create_sqs_queue(queue_name: str, client=sqs_client):
    """
    Create an SQS queue with the specified name.

    Parameters:
        queue_name (str): The name of the queue to create.
        client (boto3.client): The SQS client to use for creating the queue.

    Returns:
        dict: The response from the create_queue call.
    """
    return client.create_queue(
        QueueName=queue_name,
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '259200000'  # 3 days
        }
    )


def send_message_to_sqs(url: str, message: str, client=sqs_client):
    """
    Send a message to the specified SQS queue.

    Parameters:
        url (str): The URL of the SQS queue.
        message (str): The message to send.
        client (boto3.client): The SQS client to use for sending the message.

    Returns:
        str: The MessageId of the sent message if successful, None otherwise.
    """
    if message == "":
        error_response = {
                'Error': {
                    'Code': 'message',
                    'Message': 'Message cannot be empty',
                }
            }
        raise ClientError(error_response, "empty_message")
    try:
        response = client.send_message(
            QueueUrl=url,
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


def receive_messages_from_sqs(url: str, client=sqs_client, max_messages=10) -> list:
    """
    Receive messages from the specified SQS queue.

    Parameters:
        url (str): The URL of the SQS queue.
        client (boto3.client): The SQS client to use for receiving messages.
        max_messages (int): The maximum number of messages to receive (default is 10).

    Returns:
        list: A list of messages received from the queue.
    """
    if max_messages > 10:
        max_messages = 10
    response = client.receive_message(
        QueueUrl=url,
        MaxNumberOfMessages=max_messages,
        # WaitTimeSeconds=5  # Wait time to ensure messages are available
    )
    if "Messages" in response:
        return response["Messages"]
    else:
        return []


s3_client = boto3.client('s3', region_name='eu-west-2')
bucket_name = os.environ.get('s3_bucket')


def create_s3_bucket(bucket_name, region='eu-west-2'):
    """
    Create an S3 bucket with the specified name and region.

    Parameters:
        bucket_name (str): The name of the bucket to create.
        region (str): The region in which to create the bucket (default is 'eu-west-2').

    Returns:
        None: Creates an S3 bucket with the given name and region.
    """
    location = {'LocationConstraint': region}
    return s3_client.create_bucket(Bucket=bucket_name,
                                   CreateBucketConfiguration=location
                                   )


def upload_to_s3(file_name, bucket_name, object_name=None):
    """
    Upload a file to the specified S3 bucket.

    Parameters:
        file_name (str): The name of the file to upload.
        bucket_name (str): The name of the bucket to upload to.
        object_name (str): The name of the object in the bucket (default is the file name).

    Returns:
        None
    """
    if object_name is None:
        object_name = os.path.basename(file_name)
    return s3_client.upload_file(file_name, bucket_name, object_name)


s3 = boto3.resource('s3')
my_bucket = s3.Bucket(bucket_name)


def write_to_s3(client, data, bucket, key):
    """Helper to write material to S3."""
    body = json.dumps(data)
    try:
        client.put_object(Bucket=bucket, Key=key, Body=body)
        return True
    except ClientError as c:
        return False


def view_bucket_contents(my_bucket=my_bucket)->list:
    """
    View the contents of the specified S3 bucket.

    Parameters:
        my_bucket (boto3.resource.Bucket): The S3 bucket to view (default is my_bucket).

    Returns:
        list: A list of object keys in the bucket.
    """
    bucket_list = []
    for my_bucket_object in my_bucket.objects.all():
        bucket_list.append(my_bucket_object.key)
        print(my_bucket_object.get()['Body'].read().decode('utf-8'))

    print("My bucket contains: ", bucket_list)
    print(my_bucket)
    return bucket_list


def delete_s3_file(bucket=bucket_name, file_name='test.txt'):
    """
    Delete a file from the specified S3 bucket.

    Parameters:
        bucket (str): The name of the bucket.
        file_name (str): The name of the file to delete.

    Returns:
        None
    """
    s3.Object(bucket, file_name).delete()


def delete_all_s3_files():
    """
    Delete all files from the specified S3 bucket.

    Returns:
        None
    """
    bucket_list = []
    for my_bucket_object in my_bucket.objects.all():
        bucket_list.append(my_bucket_object.key)
        my_bucket_object.delete()


def delete_bucket(bucket_name=bucket_name):
    """
    Delete the specified S3 bucket and all its contents.

    Parameters:
        bucket_name (str): The name of the bucket to delete.

    Returns:
        None
    """
    delete_all_s3_files()
    s3_client.delete_bucket(
        Bucket=bucket_name
    )


def list_buckets():
    """
    List all S3 buckets.

    Returns:
        None
    """
    response = s3_client.list_buckets()
    for i in range(len(response['Buckets'])):
        print("Bucket:", response['Buckets'][i]['Name'])
