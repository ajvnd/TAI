import requests, pytest
from fastapi import status

from tests.integration.routers import TestBaseRouter

ENDPOINT = 'http://127.0.0.1:8000/sub_tasks'


class TestSubTaskRouter(TestBaseRouter):

    def setup_method(self, method):
        self.sub_task = {
            'task_id': 1,
            'title': 'create',
            'progress': 50,
            'pomodoros': 4,
            'is_completed': False
        }

    def teardown_method(self, method):
        if method.__name__ != 'test_can_delete_a_sub_task':
            requests.delete(f"{ENDPOINT}/{self.sub_task_id}")

    def test_can_create_sub_task(self, create_response):
        assert create_response.status_code == status.HTTP_201_CREATED

        sub_task_id = int(create_response.json())
        get_response = requests.get(f"{ENDPOINT}/{sub_task_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["title"] == self.sub_task["title"]

    def test_can_update_sub_task(self, sub_task_id):
        self.sub_task['title'] = 'updated'

        update_response = requests.put(f"{ENDPOINT}/{sub_task_id}", json=self.sub_task)
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = requests.get(f"{ENDPOINT}/{sub_task_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["title"] == self.sub_task["title"]

    def test_can_update_sub_task_progression(self, sub_task_id):
        progression = {"progress": self.sub_task["progress"] + 1}

        update_response = requests.put(f"{ENDPOINT}/{sub_task_id}/progression", json=progression)
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = requests.get(f"{ENDPOINT}/{sub_task_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["progress"] == self.sub_task['progress'] + 1

    def test_can_delete_a_sub_task(self, sub_task_id):
        delete_response = requests.delete(f"{ENDPOINT}/{sub_task_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = requests.get(f"{ENDPOINT}/{sub_task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.fixture
    def create_response(self):
        create_response = requests.post(ENDPOINT, json=self.sub_task)
        return create_response

    @pytest.fixture
    def sub_task_id(self, create_response):
        self.sub_task_id = int(create_response.json())
        return self.sub_task_id
