import pytest
import os
import boto3
from moto import mock_aws
from dotenv import load_dotenv
from utility.aws_utils import create_s3_bucket, upload_to_s3, \
    view_bucket_contents, credentials_storer, secret_retriever

load_dotenv('.env')

my_bucket = os.environ.get('s3_bucket')