import boto3
import os
from botocore.exceptions import ClientError, BotoCoreError
from dotenv import load_dotenv

load_dotenv()

region_name = "eu-west-2"

# sqs client
sqs_client = boto3.client('sqs');
def create_sqs_queue(queue_name: str, client = sqs_client):
    return client.create_queue(
        QueueName = queue_name,
        Attributes = {
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '259200000' # 3 days
        }
    )


def send_message_to_sqs(url: str, message: str, client = sqs_client):
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
    location = {'LocationConstraint': region}
    return s3_client.create_bucket(Bucket=bucket_name,
                                   CreateBucketConfiguration=location
                                   )


def upload_to_s3(file_name, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    return s3_client.upload_file(file_name, bucket_name, object_name)


s3 = boto3.resource('s3')
my_bucket = s3.Bucket(bucket_name)


def view_bucket_contents(my_bucket=my_bucket):
    bucket_list = []
    for my_bucket_object in my_bucket.objects.all():
        bucket_list.append(my_bucket_object.key)
        print(my_bucket_object.get()['Body'].read().decode('utf-8'))

    print("My bucket contains: ", bucket_list)
    print(my_bucket)
    return bucket_list


def delete_s3_file(bucket=bucket_name, file_name='test.txt'):
    s3.Object(bucket, file_name).delete()


def delete_all_s3_files():
    bucket_list = []
    for my_bucket_object in my_bucket.objects.all():
        bucket_list.append(my_bucket_object.key)
        my_bucket_object.delete()


def delete_bucket(bucket_name=bucket_name):
    delete_all_s3_files()
    s3_client.delete_bucket(
        Bucket=bucket_name
    )


def list_buckets():
    response = s3_client.list_buckets()
    for i in range(len(response['Buckets'])):
        print("Bucket:", response['Buckets'][i]['Name'])

# view_bucket_contents()
# list_buckets()
# create_s3_bucket(bucket_name)
# upload_to_s3('test.txt', bucket_name)
# upload_to_s3('test2.txt', bucket_name)


# client = boto3.client('secretsmanager', region_name='eu-west-2')


# def credentials_storer(secret_identifier, userId, password, client=client):
#     response = client.create_secret(
#         Name=secret_identifier,
#         SecretString='''{
#     "username":"userId",
#     "password":"password"
# }'''
#     )
#     print(response['Name'])


# def list_all_secrets():
#     response = client.list_secrets()
#     print(len(response['SecretList']), "secret(s) available")
#     for i in response['SecretList']:
#         print(i['Name'])


# def secret_retriever(secret_identifier):
#     secret_name = secret_identifier
#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=secret_name
#         )
#     except ClientError as e:
#         raise e

#     secret = get_secret_value_response['SecretString']
#     return secret


# def secret_delete(secret_identifier):
#     client.delete_secret(
#         SecretId=secret_identifier,
#         ForceDeleteWithoutRecovery=True
#     )
