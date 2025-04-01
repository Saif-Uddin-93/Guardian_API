import boto3, json, re, time
from botocore.exceptions import ClientError, BotoCoreError


region_name = "eu-west-2"
aws_account_id = '841162707768'
# role_name = 'guardian-iam-role'
role_arn=f'arn:aws:iam::{aws_account_id}:role/'

def sts_assume_role(role_name, role_arn=role_arn, client=None):
    # returning boto3.Session() to avoid errors with 'sts'
    return boto3
    # print(role_arn)
    # role_arn = f'{role_arn}{role_name}'
    # sts_client = client

    # try:
    #     assumed_role_object = sts_client.assume_role(
    #         RoleArn=role_arn,
    #         RoleSessionName=f'{role_name}-Session'
    #     )
    #     assumed_role_credentials = assumed_role_object['Credentials']
    # except ClientError as e:
    #     print(f"Error assuming role: {e.response['Error']['Message']}")
    #     exit(1)

    # return boto3.Session(
    #     aws_access_key_id=assumed_role_credentials['AccessKeyId'],
    #     aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],
    #     aws_session_token=assumed_role_credentials['SessionToken'],
    #     region_name=region_name
    # )

# assumed_role_session = sts_assume_role()

# CloudWatch Logs client setup
# log_stream_name = 'sqs-creation-stream'  # CloudWatch Log Stream

# Ensure log stream exists, if not, create one
def cw_log_stream(
        log_group_name,
        log_stream_name,
        client=sts_assume_role(
            role_name="cloudwatch-iam-role"
        ).client('logs', region_name=region_name)
    ):
    # print(log_group_name, log_stream_name, client)
    try:
        client.create_log_group(logGroupName=log_group_name)
        client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )
    except client.exceptions.ResourceAlreadyExistsException:
        pass  # Log stream already exists

# Function to log to CloudWatch Logs
def log_to_cloudwatch(
    role,
    message,
    log_group_name,
    log_stream_name,
):
    client=sts_assume_role(
        role_name=role,
    ).client('logs', region_name=region_name)
    # Ensure the log stream exists before starting to log
    cw_log_stream(log_group_name, log_stream_name)
    timestamp = int(time.time() * 1000)  # CloudWatch expects timestamp in milliseconds
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{
            'timestamp': timestamp,
            'message': message
        }]
    )

# iam_client = assumed_role_session.client('iam', region_name=region_name)

def create_iam_role(
        role_name: str,
        client=boto3.client('iam', region_name=region_name)
    ):
    """
    Create an IAM role with the specified client.

    Parameters:
        client (boto3.client): The IAM client to use for creating the role.

    Returns:
        tuple: The Role ID and Role ARN of the created IAM role.
    """

    # policies commented out. policies don't exist in moto3 testing suite
    # policies = [
    #     'arn:aws:iam::aws:policy/AWSLambda_FullAccess',
    #     'arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator',
    #     'arn:aws:iam::aws:policy/AmazonSQSFullAccess'
    # ]

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

    try:
        # Check if the role already exists
        try:
            existing_role = client.get_role(RoleName=role_name)
            print(f"Role {role_name} already exists.")
            return existing_role['Role']['RoleId'], existing_role['Role']['Arn']
        except client.exceptions.NoSuchEntityException:
            print(f"Role {role_name} does not exist. Creating a new role.")
        role_response = client.create_role(
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

        # for policy in policies:
        #     client.attach_role_policy(
        #         RoleName=role_name,
        #         PolicyArn=policy
        #     )

        role_arn = role_response['Role']['Arn']
        role_id = client.get_role(RoleName=role_name)['Role']['RoleId']

        return role_id, role_arn

    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']}")
        return None, None

    except BotoCoreError as e:
        print(f"BotoCoreError: {str(e)}")
        return None, None

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None, None

# sqs client
def create_sqs_queue(
        queue_name: str,
        client=sts_assume_role(
            role_name='sqs-iam-role',
        ).client('sqs', region_name=region_name),
        cw=[]):
    """
    Create an SQS queue with the specified name.

    Parameters:
        queue_name (str): The name of the queue to create.
        client (boto3.client): The SQS client to use for creating the queue.

    Returns:
        dict: The response from the create_queue call.
    """
    # Ensure the log stream exists before starting to log
    cw_log_stream(*cw)
    # Strip any leading/trailing whitespaces from the queue_name
    queue_name = queue_name.strip()
    # Validate the queue name
    if not re.match(r'^[A-Za-z0-9_-]{1,80}$', queue_name): # guardian-queue.fifo
        error_message = "Queue name can only include alphanumeric characters, hyphens, or underscores, and must be between 1 and 80 characters."
        log_to_cloudwatch('sqs-iam-role', error_message, *cw)
        raise ValueError(error_message)

    # Log the queue name being created to CloudWatch
    log_message = f"Creating queue with name: {queue_name}"
    log_to_cloudwatch("sqs-iam-role", log_message, *cw)

    # Proceed with creating the queue
    try:
        return client.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': '0',
                'MessageRetentionPeriod': '259200',  # 3 days
                'FifoQueue': 'true'
            }
        )
    except ClientError as e:
        error_message = f"Error creating queue: {e.response['Error']['Message']}"
        log_to_cloudwatch("sqs-iam-role", error_message, *cw)
        raise


def send_message_to_sqs(
        url: str,
        message: str,
        client=sts_assume_role(
            role_name='sqs-iam-role',
        ).client('sqs', region_name=region_name)
    ):
    """
    Send a message to the specified SQS queue.

    Parameters:
        url (str): The URL of the SQS queue.
        message (str): The message to send.
        client (boto3.client): The SQS client to use for sending the message.

    Returns:
        str: The MessageId of the sent message if successful, None otherwise.
    """
    if not message:
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


def receive_messages_from_sqs(
        url: str,
        client=sts_assume_role(
            role_name='sqs-iam-role',
        ).client('sqs', region_name=region_name),
        max_messages=10
    ) -> list:
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
        WaitTimeSeconds=5  # Wait time to ensure messages are available
    )
    if "Messages" in response:
        return response.get("Messages", [])
    else:
        return []


# apigateway client v1
def create_api(api_name='guardian-api'):
    apigw_client(api_name=api_name)

def apigw_client(
        integration_type='HTTP',
        api_name='guardian-api',
        client=sts_assume_role(
            role_name='apigw-iam-role',
        ).client('apigateway', region_name=region_name)
    ):

    response = None

    def api_exists(name):
        response = client.get_rest_apis()
        for item in response['items']:
            if item['name'] == name:
                return item['id']
        return None

    api_id = api_exists(api_name)

    if not api_id:
        response = client.create_rest_api(
            name = api_name,
            description = 'REST API to retrieve guardian data',
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
                'method.request.querystring.query': True,
                'method.request.querystring.queue-name': True,
                'method.request.querystring.from-date': False,
                'method.request.querystring.page-size': False,
                'method.request.querystring.star-rating': False,
            }
        )

        mapping_template = """
#set($allParams = $input.params())
{
  "status" : "200",
  "body-json" : $input.json('$'),
  "params" : {
    #foreach($type in $allParams.keySet())
      #set($params = $allParams.get($type))
      "$type" : {
        #foreach($paramName in $params.keySet())
          "$paramName" : "$util.escapeJavaScript($params.get($paramName))"
          #if($foreach.hasNext),#end
        #end
      }
      #if($foreach.hasNext),#end
    #end
  },
  "stage-variables" : {
    #foreach($key in $stageVariables.keySet())
      "$key" : "$util.escapeJavaScript($stageVariables.get($key))"
      #if($foreach.hasNext),#end
    #end
  },
  "context" : {
    "account-id" : "$context.identity.accountId",
    "api-id" : "$context.apiId",
    "api-key" : "$context.identity.apiKey",
    "authorizer-principal-id" : "$context.authorizer.principalId",
    "caller" : "$context.identity.caller",
    "cognito-authentication-provider" : "$context.identity.cognitoAuthenticationProvider",
    "cognito-authentication-type" : "$context.identity.cognitoAuthenticationType",
    "cognito-identity-id" : "$context.identity.cognitoIdentityId",
    "cognito-identity-pool-id" : "$context.identity.cognitoIdentityPoolId",
    "http-method" : "$context.httpMethod",
    "stage" : "$context.stage",
    "source-ip" : "$context.identity.sourceIp",
    "user" : "$context.identity.user",
    "user-agent" : "$context.identity.userAgent",
    "user-arn" : "$context.identity.userArn",
    "request-id" : "$context.requestId",
    "resource-id" : "$context.resourceId",
    "resource-path" : "$context.resourcePath"
  }
}
"""

        client.put_integration(
            restApiId=api_id,
            resourceId=root_id,
            httpMethod='GET',
            type=integration_type,
            requestTemplates={
                'application/json': mapping_template
            }
        )

    try:
        client.create_deployment(restApiId=api_id, stageName='dev')
    except ClientError as e:
        print(f"Error creating deployment: {e.response['Error']['Message']}")


    return client, api_id


# # lambda client
# def create_lambda(
#         role_arn:str=role_arn,
#         client=sts_assume_role().client('lambda', region_name=region_name)
#     ):
#     # Create functions
#     with open('sqs_send.zip', 'rb') as f:
#         sqs_send_code = f.read()

#     with open('sqs_receive.zip', 'rb') as f:
#         sqs_receive_code = f.read()

#     client.create_function(
#         FunctionName='sqs_send',
#         Runtime='python3.13',
#         Role=role_arn,
#         Handler='sqs_send.lambda_handler',
#         Code={
#             'ZipFile': sqs_send_code
#         },
#         Description='Send a message to an SQS queue'
#     )

#     client.create_function(
#         FunctionName='sqs_receive',
#         Runtime='python3.13',
#         Role=role_arn,
#         Handler='sqs_receive.lambda_handler',
#         Code={
#             'ZipFile': sqs_receive_code
#         },
#         Description='Receive messages from an SQS queue'
#     )

#     # Create layers
#     with open('requests_layer.zip', 'rb') as f:
#         requests_code = f.read()

#     with open('utility_layer.zip', 'rb') as f:
#         utility_code = f.read()

#     client.publish_layer_version(
#         LayerName='requests',
#         Description='Layer containing requests module',
#         Content={
#             'ZipFile': requests_code
#         }
#     )

#     client.publish_layer_version(
#         LayerName='utility',
#         Description='Layer containing utility module',
#         Content={
#             'ZipFile': utility_code
#         }
#     )

