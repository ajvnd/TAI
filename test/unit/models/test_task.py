from src import models


class TestTask:

    def setup_method(self, method):
        self.task = models.Task()

    def test_generate_tasks_function_should_generate_correct_info_for_their_fields(self):
        task = self.task.generate_tasks()

        assert task.project_id == 1
        assert task.is_completed is not None
        assert task.title is not None
