import boto3

# Initialize the API Gateway V2 client
api_client = boto3.client('apigatewayv2')

# Define the API ID and other details
api_id = 'your-api-id'
route_key = 'GET /items'
target = 'integrations/your-integration-id'

# Define the route request parameters
route_request_parameters = {
    'param1': {'Required': True},
    'param2': {'Required': False}
}

# Create the route with request parameters
response = api_client.create_route(
    ApiId=api_id,
    RouteKey=route_key,
    Target=target,
    RequestParameters=route_request_parameters
)

