def test_api_gateway_creation(apigw_client_fixture):
    client, api_id = apigw_client_fixture
    
    assert client.get_rest_api(restApiId=api_id)['name'] == 'guardian-api'

def test_api_method_type_get(apigw_client_fixture):
    client, api_id = apigw_client_fixture

    response = client.get_resources(restApiId=api_id)
    assert response['items'][0]['path'] == '/'
    assert response['items'][0]['resourceMethods']['GET']['httpMethod'] == 'GET'


    