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


# mock api gateway v2 client
@pytest.fixture()
def apigwv2_client(aws_credentials):
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

        yield client, api_id


# mock apigateway client v1
@pytest.fixture()
def apigw_client(aws_credentials):
    with mock_aws():
        client = boto3.client('apigateway', region_name='eu-west-2')

        api_name = 'guardianAPI'
        api_id = None
        response = None

        def api_exists(name):
            response = client.get_rest_apis()
            for item in response['items']:
                if item['name'] == name:
                    return True
            return False
        
        if not api_exists(api_name):

            response = client.create_rest_api(
                name = api_name,
                description = 'Example REST API',
                endpointConfiguration = {
                    'types': ['REGIONAL']
                }
            )
            api_id = response['id']

            resources = client.get_resources(restApiId=api_id)
            root_id = resources['items'][0]['id']

            client.create_usage_plan(
                name='Daily',
                description='50 api calls per day',
                quota={
                    'limit': 50,
                    'period': 'DAY'
                }
            )

            client.put_method(
                restApiId=api_id,
                resourceId=root_id,
                httpMethod='GET',
                authorizationType='NONE',
                requestParameters={
                    'method.request.querystring.name': True,
                    'method.request.querystring.param2': False
                }
            )
            
            client.put_integration(
                restApiId=api_id,
                resourceId=root_id,
                httpMethod='GET',
                type='MOCK',
                requestTemplates={
                    'application/json': '{"statusCode": 200}'
                }
            )
        else:
            for item in response['items']:
                if item['name'] == api_name:
                    api_id = item['id']

        yield client, api_id


@pytest.fixture()
def secretsmanager_client(aws_credentials):
    with mock_aws():
        yield boto3.client("secretsmanager")