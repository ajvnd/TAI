from src import models


class TestTaskModel:

    def setup_method(self, method):
        self.task = models.TaskModel()

    def test_can_generate_tasks_and_populate_correct_info_for_their_fields(self):
        task = self.task.generate_tasks()

        assert task.project_id == 1
        assert task.is_completed is not None
        assert task.title is not None
