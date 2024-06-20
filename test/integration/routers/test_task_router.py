import requests, pytest
from fastapi import status

ENDPOINT = 'http://127.0.0.1:8000/tasks'


class TestTaskRouter:
    def setup_method(self, method):
        self.task = {
            'project_id': 1,
            'title': 'create',
            'is_completed': True,
        }

    def teardown_method(self, method):
        if method.__name__ != 'test_can_delete_a_task':
            requests.delete(f"{ENDPOINT}/{self.task_id}")

    def test_can_create_a_task(self, create_response):
        assert create_response.status_code == status.HTTP_201_CREATED

        task_id = int(create_response.json())
        get_response = requests.get(f"{ENDPOINT}/{task_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()['title'] == self.task['title']

    def test_can_update_a_task(self, task_id):
        self.task['title'] = 'updated'

        update_response = requests.put(f"{ENDPOINT}/{task_id}", json=self.task)
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = requests.get(f"{ENDPOINT}/{task_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()['title'] == self.task['title']

    def test_can_delete_a_task(self, task_id):
        delete_response = requests.delete(f"{ENDPOINT}/{task_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = requests.get(f"{ENDPOINT}/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.fixture
    def create_response(self):
        create_response = requests.post(ENDPOINT, json=self.task)
        return create_response

    @pytest.fixture
    def task_id(self, create_response):
        self.task_id = int(create_response.json())
        return self.task_id
