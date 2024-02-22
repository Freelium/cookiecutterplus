import pytest
from unittest.mock import patch, MagicMock
from cookiecutterplus import CookieCutterPlus

@pytest.fixture
def mock_determine_repo_dir():
    with patch('cookiecutter.repository.determine_repo_dir') as mock:
        yield mock

@pytest.fixture
def mock_cookiecutter():
    with patch('cookiecutter.main.cookiecutter') as mock:
        yield mock

def test_cookiecutter_plus_skinny_runs(mock_determine_repo_dir, mock_cookiecutter):
    # Setup mock return values
    mock_determine_repo_dir.return_value = ("mock_template_path", "mock_repo_dir")
    mock_cookiecutter.return_value = None  # Assuming cookiecutter returns None for success

    # Define your test payload and output path
    test_payload = {
        "template1": {
            "template_path": "cookiecutter/shared/cookiecutter-gha",
            "context_vars": {"key1": "value1", "key2": "value2"}
        }
    }
    test_output_path = "test/output/path"

    # Instantiate and run your class
    ccp = CookieCutterPlus(payload=test_payload, output_path=test_output_path)
    ccp.run()

    # Assertions
    mock_determine_repo_dir.assert_called_once_with(
        template=ccp.github_repo_prefix,
        directory="cookiecutter/shared/cookiecutter-gha",
        checkout="main",
        clone_to_dir="./template_repo",
        no_input=True,
        abbreviations="gh"
    )
    mock_cookiecutter.assert_called_once_with(
        template="mock_template_path",
        no_input=True,
        overwrite_if_exists=True,
        extra_context={"key1": "value1", "key2": "value2"},
        output_dir=test_output_path
    )
