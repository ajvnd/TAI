from src import models


class TestProjectModel:

    def setup_method(self, method):
        self.project = models.ProjectModel()

    def test_can_generate_projects_and_populate_correct_info_for_their_fields(self):
        project = self.project.generate_projects()

        assert project.title is not None
