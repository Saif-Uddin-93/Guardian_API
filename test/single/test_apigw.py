import pytest

# def test_create_route_minimal(apigw_client):
#     api_id = apigw_client.create_api(Name="test-api", ProtocolType="HTTP")["ApiId"]
#     resp = apigw_client.create_route(ApiId=api_id, RouteKey="GET /")
#     print(resp)

#     assert resp["ApiKeyRequired"] is False
#     assert resp["AuthorizationType"] == "NONE"
#     assert "RouteId" in resp
#     assert resp["RouteKey"] == "GET /"
#     assert "AuthorizationScopes" not in resp
#     assert "AuthorizerId" not in resp
#     assert "ModelSelectionExpression" not in resp
#     assert "OperationName" not in resp
#     assert "RequestModels" not in resp
#     assert "RouteResponseSelectionExpression" not in resp
#     assert "Target" not in resp



@pytest.mark.xfail
def test_create_route_minimal(apigw_client):
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
    response = apigw_client.create_route(
        ApiId=api_id,
        RouteKey=route_key,
        Target=target,
        RequestParameters=route_request_parameters
    )

    # Print the response
    print(response)
    assert False