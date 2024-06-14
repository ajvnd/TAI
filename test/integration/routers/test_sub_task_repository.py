import requests

ENDPOINT = 'http://127.0.0.1:8000/sub_tasks'


class TestSubTaskRepository:

    def setup_method(self):
        self.sub_task = {
            'task_id': 1,
            'title': 'create',
            'spend': 50,
            'duration': 100,
            'is_completed': False
        }

    def test_can_create_sub_task(self):
        create_response = requests.post(ENDPOINT, json=self.sub_task)
        assert create_response.status_code == 201

        sub_task_id = int(create_response.json())

        get_response = requests.get(f"{ENDPOINT}/{sub_task_id}")
        assert get_response.json()["title"] == "create"

    def test_can_update_sub_task(self):
        create_response = requests.post(ENDPOINT, json=self.sub_task)
        sub_task_id = int(create_response.json())

        self.sub_task['title'] = 'update'
        update_response = requests.put(f"{ENDPOINT}/{sub_task_id}", json=self.sub_task)

        assert update_response.status_code == 204

        get_response = requests.get(f"{ENDPOINT}/{sub_task_id}")
        assert get_response.json()["title"] == "update"

    def test_can_update_sub_task_progression(self):
        create_response = requests.post(ENDPOINT, json=self.sub_task)
        sub_task_id = int(create_response.json())

        update_response = requests.put(f"{ENDPOINT}/{sub_task_id}/progression",
                                       json={'spend': self.sub_task['spend'] + 1})

        assert update_response.status_code == 204

        get_response = requests.get(f"{ENDPOINT}/{sub_task_id}")

        assert get_response.json()["spend"] == self.sub_task['spend'] + 1
