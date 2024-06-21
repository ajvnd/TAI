import requests

ENDPOINT = 'http://127.0.0.1:8000'


class TestBaseRouter:
    def test_can_connect_to_endpoints(url):
        response = requests.get(ENDPOINT)
        assert response.json()["detail"] == "Not Found"
