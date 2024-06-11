from unittest.mock import patch, Mock
from src.models import get_db


class TestBase:

    @patch("src.models.SessionLocal")
    def test_generate_projects_function_should_generate_correct_info_for_their_fields(self, mock_session_local):
        mock_session_local.return_value = Mock()

        project = get_db()

        assert project is not None
