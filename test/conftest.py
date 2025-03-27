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


# mock client
@pytest.fixture()
def boto3_fixture(aws_credentials):
    with mock_aws():
        yield boto3


# mock iam client
@pytest.fixture()
def iam_client_fixture(boto3_fixture):
    with mock_aws():
        client = boto3_fixture.client('iam', region_name='eu-west-2')
        role_name='guardian-iam-role'

        trust_policy_doc = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "lambda.amazonaws.com"
                        ]
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        })

        
        # Check if the role already exists
        try:
            existing_role = client.get_role(RoleName=role_name)
            print(f"Role {role_name} already exists.")
            return existing_role['Role']['RoleId'], existing_role['Role']['Arn']
        except client.exceptions.NoSuchEntityException:
            print(f"Role {role_name} does not exist. Creating a new role.")
        client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=trust_policy_doc
        )

        permissions_policy_doc = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "lambda:*",
                        "sqs:*",
                        "sqs:CreateQueue",
                        "sqs:GetQueueAttributes",
                        "apigateway:*",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "*"
                }
            ]
        })

        # Create and attach the permissions policy
        policy_response = client.create_policy(
            PolicyName=f'{role_name}-policy',
            PolicyDocument=permissions_policy_doc
        )

        policy_arn = policy_response['Policy']['Arn']

        client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )

        yield boto3_fixture, client


# mock sts client
@pytest.fixture()
def sts_client_fixture(iam_client_fixture):
    with mock_aws():
        boto3_fixture, _ = iam_client_fixture
        yield sts_assume_role("role_arn", boto3_fixture.client("sts", region_name="eu-west-2"))


# mock sqs client
@pytest.fixture()
def sqs_client_fixture(sts_client_fixture):
    with mock_aws():
        yield sts_client_fixture.client("sqs")


# mock lambda client
@pytest.fixture()
def lambda_client_fixture(sts_client_fixture):
    with mock_aws():
        yield sts_client_fixture.client('lambda')


# mock apigateway client v1
@pytest.fixture()
def apigw_client_fixture(sts_client_fixture):
    with mock_aws():
        response = apigw_client(
            integration_type='MOCK',
            client=sts_client_fixture.client('apigateway'))
        client, api_id = response
        yield client, api_id


# mock cloudwatch logs client
@pytest.fixture()
def cw_logs_client_fixture(sts_client_fixture):
    with mock_aws():
        yield sts_client_fixture.client('logs')

