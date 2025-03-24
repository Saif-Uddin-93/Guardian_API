import pytest, boto3, os
from moto import mock_aws
from utility.aws_utils import *


# mock aws credentials
@pytest.fixture()
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


# mock sqs client
@pytest.fixture()
def sqs_client_fixture(aws_credentials):
    with mock_aws():
        yield boto3.client("sqs")


# mock lambda client
@pytest.fixture()
def lambda_client_fixture(aws_credentials):
    with mock_aws():
        yield boto3.client('lambda')


# mock apigateway client v1
@pytest.fixture()
def apigw_client_fixture(aws_credentials):
    with mock_aws():
        response = apigw_client('MOCK')
        client, api_id = response
        yield client, api_id


# mock cloudwatch logs client
@pytest.fixture()
def cw_logs_client_fixture(aws_credentials):
    with mock_aws():
        yield boto3.client('logs')


# # mock api gateway v2 client
# @pytest.fixture()
# def apigwv2_client(aws_credentials):
#     with mock_aws():
#         client = boto3.client('apigatewayv2')
        
#         response = client.create_api(
#             Name='TestAPI',
#             ProtocolType='HTTP'
#         )
#         api_id = response['ApiId']
        
#         route_request_parameters = {
#             'name': {'Required': True},
#             'param2': {'Required': False}
#         }

#         client.create_route(
#             ApiId=api_id,
#             RouteKey='GET /test',
#             # Target=target,
#             RequestParameters=route_request_parameters
#         )
        
#         client.create_integration(
#             ApiId=api_id,
#             IntegrationType='MOCK',
#             IntegrationUri='lambda'
#         )

#         yield client, api_id


# @pytest.fixture()
# def secretsmanager_client(aws_credentials):
#     with mock_aws():
#         yield boto3.client("secretsmanager")