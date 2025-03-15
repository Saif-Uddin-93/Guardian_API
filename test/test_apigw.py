import pytest


def test_api_gateway_creation(apigw_client):
    client, api_id = apigw_client
    
    assert client.get_rest_api(restApiId=api_id)['name'] == 'guardianAPI'

def test_send_api_request(apigw_client):
    client, api_id = apigw_client

    response = client.get_resources(restApiId=api_id)
    assert response['items'][0]['path'] == '/'
    assert response['items'][0]['resourceMethods']['GET']['httpMethod'] == 'GET'

    def test_invoke_api_method(apigw_client):
        client, api_id = apigw_client

        # invoke_url = f'https://{api_id}.execute-api.eu-west-2.amazonaws.com/test/'
        response = client.test_invoke_method(
            restApiId=api_id,
            resourceId=client.get_resources(restApiId=api_id)['items'][0]['id'],
            httpMethod='GET'
        )

        print(response)

        assert response['status'] == 200
        assert 'body' in response