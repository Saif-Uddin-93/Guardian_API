import pytest, boto3, os
from moto import mock_aws


# mock aws credentials
@pytest.fixture()
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    # os.environ["AWS_SECURITY_TOKEN"] = "testing"
    # os.environ["AWS_SESSION_TOKEN"] = "testing"
    # os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


# mock s3 client
@pytest.fixture()
def s3_client(aws_credentials):
    with mock_aws():
        yield boto3.client("s3")


# mock sqs client
@pytest.fixture()
def sqs_client(aws_credentials):
    with mock_aws():
        yield boto3.client("sqs")


# mock s3 client with bucket
@pytest.fixture()
def s3_buckets(s3_client):
    s3_client.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )
    return s3_client


# mock api gateway client
@pytest.fixture
def apigw_client(aws_credentials):
    with mock_aws():
        client = boto3.client('apigatewayv2')
        
        response = client.create_api(
            Name='TestAPI',
            ProtocolType='HTTP'
        )
        api_id = response['ApiId']
        
        route_request_parameters = {
            'name': {'Required': True},
            'param2': {'Required': False}
        }

        client.create_route(
            ApiId=api_id,
            RouteKey='GET /test',
            # Target=target,
            RequestParameters=route_request_parameters
        )
        
        client.create_integration(
            ApiId=api_id,
            IntegrationType='MOCK',
            IntegrationUri='lambda'
        )

        client.create_usage_plan(
            name='Daily',
            description='50 calls per day',
            quota={
                'limit': 50,
                'period': 'DAY'
            }
        )

        yield client, api_id


@pytest.fixture()
def secretsmanager_client(aws_credentials):
    with mock_aws():
        yield boto3.client("secretsmanager")