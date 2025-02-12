import pytest, json, boto3, os, pika
from moto import mock_aws
from dotenv import load_dotenv


def test_connect_to_rabbitmq_server():
    pass