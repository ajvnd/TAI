import requests

ENDPOINT = 'http://127.0.0.1:8000/projects'


class TestProjectRepository:

    def test_can_create_a_new_project(self):
        create_response = requests.post(ENDPOINT, json={'title': 'test'})
        assert create_response.status_code == 201

        project_id = int(create_response.json())

        get_response = requests.get(f"{ENDPOINT}/{project_id}")
        assert get_response.json()["title"] == "test"

    def test_can_update_a_new_project(self):
        create_response = requests.post(ENDPOINT, json={'title': 'test'})
        project_id = int(create_response.json())

        update_response = requests.put(f"{ENDPOINT}/{project_id}", json={'title': 'test_updated'})
        assert update_response.status_code == 204

        get_response = requests.get(f"{ENDPOINT}/{project_id}")
        assert get_response.json()["title"] == "test_updated"

    def test_can_delete_a_new_project(self):
        create_response = requests.post(ENDPOINT, json={'title': 'test'})
        project_id = int(create_response.json())

        delete_response = requests.delete(f"{ENDPOINT}/{project_id}")
        assert delete_response.status_code == 204

        get_response = requests.get(f"{ENDPOINT}/{project_id}")
        assert get_response.status_code == 404
