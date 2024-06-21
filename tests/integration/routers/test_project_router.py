import pytest
import requests
from fastapi import status

from tests.integration.routers import TestBaseRouter

ENDPOINT = 'http://127.0.0.1:8000/projects'


class TestProjectRouter(TestBaseRouter):

    def setup_method(self, method):
        self.project = {'title': 'create'}

    def teardown_method(self, method):
        if method.__name__ != 'test_can_delete_a_project':
            requests.delete(f"{ENDPOINT}/{self.project_id}")

    def test_can_create_a_new_project(self, create_response):
        assert create_response.status_code == status.HTTP_201_CREATED

        project_id = int(create_response.json())
        get_response = requests.get(f"{ENDPOINT}/{project_id}")
        assert get_response.json()["title"] == self.project["title"]
        assert get_response.status_code == status.HTTP_200_OK

    def test_can_update_a_project(self, project_id):
        self.project['title'] = 'update'
        update_response = requests.put(f"{ENDPOINT}/{project_id}", json=self.project)
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = requests.get(f"{ENDPOINT}/{project_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["title"] == "update"

    def test_can_delete_a_project(self, project_id):
        delete_response = requests.delete(f"{ENDPOINT}/{project_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = requests.get(f"{ENDPOINT}/{project_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.fixture
    def create_response(self):
        create_response = requests.post(ENDPOINT, json=self.project)
        return create_response

    @pytest.fixture
    def project_id(self, create_response):
        self.project_id = int(create_response.json())
        return self.project_id
