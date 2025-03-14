import pytest


def test_api_gateway_creation(apigw_client):
    client, api_id = apigw_client
    
    assert client.get_rest_api(restApiId=api_id)['name'] == 'guardianAPI'