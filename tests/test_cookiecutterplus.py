import yaml, pytest, requests
from jsonschema import ValidationError
from cookiecutterplus import CookieCutterPlus
from unittest.mock import patch, MagicMock


# Import the persistencebuilder from cookiecutterplus class
@patch('cookiecutterplus.cookiecutterplus.PersistenceBuilder.get_persister')
# Test the CookieCutterPlusAPI with a persistence payload included
def test_cookiecutter_persistence(mock_get_persister, tmp_path):
    cookiecutterplus_payload = {
        "template_payload": {
            "gha": {
                "template_context": "tests/fixtures/basic-backwards",
                "template_path": "",
                "context_vars": {
                    "component_name": "My Cut Cookie",
                    "project_name": "my-cut-cookie",
                    "project_slug": "my-cut-cookie"
                }
            },
        },
        "output_path": f"{tmp_path}",
        "no_input": True,
        "persistence": {
            "gh": {
                "destination": "test/repo",
                "repo_type": "private"
            }
        }
    }
    mock_persistence_instance = MagicMock()
    mock_get_persister.return_value = mock_persistence_instance
    # Instantiate and run your class
    ccp = CookieCutterPlus(test_payload)
    ccp.run()
    # Assert template was created
    dir = tmp_path / "my-cut-cookie"
    simple_yaml_file = dir / "simple.yaml"

    assert dir.is_dir()
    assert simple_yaml_file.is_file()
    with open(simple_yaml_file) as f:
        data = yaml.safe_load(f)
        assert data == {
            "name": "my-cut-cookie",
            "additive": "this is additive"
        }
    # Assert the persistence was called
    mock_persistence_instance.persist.assert_called_once()


def test_cookiecutter_basic_backwards_compat(tmp_path):
    test_payload = {
        "output_path": tmp_path,
        "template_payload": {
            "gha": {
                "template_context": "tests/fixtures/basic-backwards",
                "template_path": "",
                "context_vars": {
                    "component_name": "My Cut Cookie",
                    "project_name": "my-cut-cookie",
                    "project_slug": "my-cut-cookie"
                }
            }
        },
        "no_input": True
    }

    # Instantiate and run your class
    ccp = CookieCutterPlus(test_payload)
    ccp.run()

    dir = tmp_path / "my-cut-cookie"
    simple_yaml_file = dir / "simple.yaml"

    assert dir.is_dir()
    assert simple_yaml_file.is_file()
    with open(simple_yaml_file) as f:
        data = yaml.safe_load(f)
        assert data == {"name": "my-cut-cookie"}

def test_cookiecutter_basic(tmp_path):
    test_payload = {
        "output_path": tmp_path,
        "template_payload": {
            "gha": {
                "template_context": "tests/fixtures/basic",
                "template_path": "",
                "context_vars": {
                    "component_name": "My Cut Cookie",
                    "project_name": "my-cut-cookie",
                    "project_slug": "my-cut-cookie",
                },
                "ccplus": {
                    "additive": "this is additive"
                }
            }
        },
        "no_input": True
    }

    # Instantiate and run your class
    ccp = CookieCutterPlus(test_payload)
    ccp.run()

    dir = tmp_path / "my-cut-cookie"
    simple_yaml_file = dir / "simple.yaml"

    assert dir.is_dir()
    assert simple_yaml_file.is_file()
    with open(simple_yaml_file) as f:
        data = yaml.safe_load(f)
        assert data == {
            "name": "my-cut-cookie",
            "additive": "this is additive"
        }

def test_cookiecutter_basic_invalid_additive(tmp_path):
    test_payload = {
        "output_path": tmp_path,
        "template_payload": {
            "gha": {
                "template_context": "tests/fixtures/basic",
                "template_path": "",
                "context_vars": {
                    "component_name": "My Cut Cookie",
                    "project_name": "my-cut-cookie",
                    "project_slug": "my-cut-cookie",
                },
                "ccplus": {
                    "invalid_attribute": "this should fail :("
                }
            }
        },
        "no_input": True
    }

    # Instantiate and run your class
    ccp = CookieCutterPlus(test_payload)
    with pytest.raises(ValidationError) as exc_info:
        ccp.run()
    print(f'error value {exc_info.value}')
    assert str(exc_info.value).startswith("'additive' is a required property")
