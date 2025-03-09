# import json
# import boto3
# import pytest
# import zipfile
# import io
# from moto import mock_aws

# LAMBDA_FUNCTION_NAME = "TestLambdaFunction"
# API_NAME = "TestAPI"

# # Function to create a ZIP package for Lambda
# def create_lambda_zip():
#     lambda_code = """ 
# import json

# def lambda_handler(event, context):
#     query_params = event.get("queryStringParameters", {})
#     name = query_params.get("name", "Guest")
#     return {
#         "statusCode": 200,
#         "body": json.dumps({"message": f"Hello, {name}!"})
#     }
# """
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
#         zf.writestr("lambda_function.py", lambda_code)
#     zip_buffer.seek(0)
#     return zip_buffer.read()

# @pytest.fixture
# def setup_mock_aws():
#     """Mock AWS services including IAM, API Gateway, and Lambda."""
#     with mock_aws():
#         # Create AWS clients
#         iam_client = boto3.client("iam", region_name="us-east-1")
#         lambda_client = boto3.client("lambda", region_name="us-east-1")
#         apigateway_client = boto3.client("apigateway", region_name="us-east-1")

#         # ✅ CREATE A MOCK IAM ROLE
#         assume_role_policy = json.dumps({
#             "Version": "2012-10-17",
#             "Statement": [{
#                 "Effect": "Allow",
#                 "Principal": {"Service": "lambda.amazonaws.com"},
#                 "Action": "sts:AssumeRole"
#             }]
#         })

#         role_response = iam_client.create_role(
#             RoleName="TestLambdaRole",
#             AssumeRolePolicyDocument=assume_role_policy,
#         )
#         role_arn = role_response["Role"]["Arn"]

#         # ✅ CREATE A MOCK LAMBDA FUNCTION WITH A VALID IAM ROLE
#         lambda_response = lambda_client.create_function(
#             FunctionName=LAMBDA_FUNCTION_NAME,
#             Runtime="python3.8",
#             Role=role_arn,  # Pass the newly created IAM role
#             Handler="lambda_function.lambda_handler",
#             Code={"ZipFile": create_lambda_zip()},
#         )
#         lambda_arn = lambda_response["FunctionArn"]

#         # ✅ CREATE A MOCK API GATEWAY
#         api_response = apigateway_client.create_rest_api(
#             name=API_NAME, description="Mocked API Gateway for testing"
#         )
#         api_id = api_response["id"]

#         # Get Root Resource ID
#         resources = apigateway_client.get_resources(restApiId=api_id)
#         root_id = resources["items"][0]["id"]

#         # Create a new resource under root (e.g., `/test`)
#         resource_response = apigateway_client.create_resource(
#             restApiId=api_id,
#             parentId=root_id,
#             pathPart="test",
#         )
#         resource_id = resource_response["id"]

#         # Create a GET method with query parameters
#         apigateway_client.put_method(
#             restApiId=api_id,
#             resourceId=resource_id,
#             httpMethod="GET",
#             authorizationType="NONE",
#             requestParameters={"method.request.querystring.name": True},
#         )

#         # Integrate API Gateway with Lambda
#         apigateway_client.put_integration(
#             restApiId=api_id,
#             resourceId=resource_id,
#             httpMethod="GET",
#             type="AWS_PROXY",
#             integrationHttpMethod="POST",
#             uri=f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations",
#         )

#         yield lambda_client, apigateway_client, api_id, lambda_arn


# def test_lambda_invocation(setup_mock_aws):
#     """Test if API Gateway triggers Lambda correctly by simulating an event."""
#     lambda_client, apigateway_client, api_id, lambda_arn = setup_mock_aws

#     # Simulate API Gateway event payload with query parameters
#     api_gateway_event = {
#         "queryStringParameters": {"name": "John"}
#     }

#     # Invoke Lambda as if API Gateway triggered it
#     response = lambda_client.invoke(
#         FunctionName=LAMBDA_FUNCTION_NAME,
#         Payload=json.dumps(api_gateway_event),
#     )

#     # ✅ Check if Payload is empty
#     payload_content = response["Payload"].read().decode()
#     assert payload_content, "Lambda response payload is empty!"

#     # ✅ Load only if valid JSON
#     response_payload = json.loads(payload_content)

#     # Verify the invocation was successful
#     assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
#     assert response_payload["statusCode"] == 200
#     assert json.loads(response_payload["body"])["message"] == "Hello, John!"


def test_create_route_minimal(apigw_client):
    api_id = apigw_client.create_api(Name="test-api", ProtocolType="HTTP")["ApiId"]
    resp = apigw_client.create_route(ApiId=api_id, RouteKey="GET /")

    assert resp["ApiKeyRequired"] is False
    assert resp["AuthorizationType"] == "NONE"
    assert "RouteId" in resp
    assert resp["RouteKey"] == "GET /"
    assert "AuthorizationScopes" not in resp
    assert "AuthorizerId" not in resp
    assert "ModelSelectionExpression" not in resp
    assert "OperationName" not in resp
    assert "RequestModels" not in resp
    assert "RouteResponseSelectionExpression" not in resp
    assert "Target" not in resp