import pytest
from src import models


class TestSubTask:

    def setup_method(self, method):
        self.sub_task = models.SubTask()

    @pytest.mark.parametrize("number_of_tasks", [10, 20])
    def test_generate_sub_tasks_function_to_generate_correct_number_of_items(self, number_of_tasks):
        sub_tasks = self.sub_task.generate_sub_tasks(number_of_tasks)
        assert len(sub_tasks) == number_of_tasks

    def test_generate_sub_tasks_function_to_generate_correct_info_for_their_fields(self):
        sub_tasks = self.sub_task.generate_sub_tasks()

        for sub_task in sub_tasks:
            assert sub_task.task_id == 1
            assert sub_task.title is not None
            assert sub_task.spend is not None
            assert sub_task.duration is not None
            assert sub_task.is_completed is not None
