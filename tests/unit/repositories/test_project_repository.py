import pytest
from unittest.mock import MagicMock

from src.models import ProjectModel
from src.repositories import ProjectRepository


class TestProjectRepository:

    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()

    def test_can_get_a_project(self, mock_db_session):
        # Arrange
        project_repository = ProjectRepository(mock_db_session)
        mock_project = ProjectModel(id=1, title="Test Project")
        mock_db_session.query().filter().first.return_value = mock_project

        # Act
        project = project_repository.get_project(1)

        # Assert
        mock_db_session.query.assert_called_once(ProjectModel)
        mock_db_session.query().filter.assert_called_once(ProjectModel.id == 1)
        mock_db_session.query().filter().first.assert_called_once()

        assert project is not None
        assert project.id == 1
        assert project.title == "Test Project"

    def test_can_get_all_projects(self, mock_db_session):
        # Arrange
        project_repository = ProjectRepository(mock_db_session)
        mock_projects = [ProjectModel(id=1, title="Test Project")]
        mock_db_session.query().filter().all.return_value = mock_projects

        # Act
        projects = project_repository.get_projects()

        # Assert
        mock_db_session.query.assert_called_once(ProjectModel)
        mock_db_session.query().all.assert_called_once()

        assert projects is not None
        assert projects[0].id == 1
        assert projects[0].title == "Test Project"

    def test_can_create_a_project(self, mock_db_session):
        # Arrange
        project_repository = ProjectRepository(mock_db_session)
        mock_project = ProjectModel(id=1, title="Test Project")

        # Act
        project_repository.create_project(mock_project)

        # Assert
        mock_db_session.add.assert_called_once(mock_project)

    def test_can_update_project(self, mock_db_session):
        project_repository = ProjectRepository(mock_db_session)
        mock_project = ProjectModel(id=1, title="Test Project")

        project_repository.update_project(mock_project)

        # TODO: Inner funnction should be patch
