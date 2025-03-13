import json

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


def test_api_gatewayv2_query_params(apigwv2_client):
    client, api_id = apigwv2_client
    
    assert True