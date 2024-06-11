from src import models


class TestProject:

    def setup_method(self, method):
        self.project = models.Project()

    def test_generate_projects_function_should_generate_correct_info_for_their_fields(self):
        project = self.project.generate_projects()

        assert project.title is not None
