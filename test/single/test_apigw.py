import pytest


def test_api_gatewayv2_query_params(apigwv2_client):
    client, api_id = apigwv2_client
    
    assert True