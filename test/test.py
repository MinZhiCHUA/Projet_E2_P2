from test.conftest import client
def test_should_status_code_homepage(client):
        response = client.get('/')
        assert response.status_code == 200