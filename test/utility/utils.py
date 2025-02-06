import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv('.env')

region_name = "eu-west-2"

client = boto3.client('secretsmanager', region_name='eu-west-2')


def credentials_storer(secret_identifier, userId, password, client=client):
    response = client.create_secret(
        Name=secret_identifier,
        SecretString='''{
    "username":"userId",
    "password":"password"
}'''
    )
    print(response['Name'])


def list_all_secrets():
    response = client.list_secrets()
    print(len(response['SecretList']), "secret(s) available")
    for i in response['SecretList']:
        print(i['Name'])


def secret_retriever(secret_identifier):
    secret_name = secret_identifier
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return secret


def secret_delete(secret_identifier):
    client.delete_secret(
        SecretId=secret_identifier,
        ForceDeleteWithoutRecovery=True
    )


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
