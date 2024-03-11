import json, pytest, requests
from unittest.mock import patch, MagicMock
from api import CookieCutterPlusAPI

# Create a fixture to instantiate a Flask test client with the CookieCutterPlusAPI
@pytest.fixture
def client():
   api = CookieCutterPlusAPI()
   app = api.get_flask_app()
   app.config['TESTING'] = True
   with app.test_client() as client:
       yield client 

# Test the CookieCutterPlusAPI with a valid payload
def test_cookiecutter_api_success(tmp_path, client):
    cookiecutterplus_payload = {
        "template_payload": {
            "gha": {
                "template_context": "fixtures/basic-backwards",
                "template_path": "",
                "context_vars": {
                    "component_name": "My Cut Cookie",
                    "project_name": "my-cut-cookie",
                    "project_slug": "my-cut-cookie"
                }
            },
        },
        "output_path": f"{tmp_path}",
        "no_input": True
    }
    # Send a POST request to the API
    response = client.post('/generate', json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 201

# Test the CookieCutterPlusAPI with an invalid parameter included in the payload
def test_cookiecutter_api_invalid_parameter(tmp_path, client):
    api = CookieCutterPlusAPI()
    cookiecutterplus_payload = {
        "template_payload": {
            "gha": {
                "template_context": "fixtures/basic-backwards",
                "template_path": "",
                "context_vars": {
                    "component_name": "My Cut Cookie",
                    "project_name": "my-cut-cookie",
                    "project_slug": "my-cut-cookie"
                }
            },
        },
        "ccplus": {
            "badParameter": "badValue"
        },
        "output_path": f"{tmp_path}",
        "no_input": True
    }
    # Send a POST request to the API
    response = client.post('/generate', json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 400

# Import the persistencebuilder from cookiecutterplus class
@patch('cookiecutterplus.cookiecutterplus.PersistenceBuilder.get_persister')
# Test the CookieCutterPlusAPI with a persistence payload included
def test_cookiecutter_api_persistence(mock_get_persister, client, tmp_path):
    cookiecutterplus_payload = {
        "template_payload": {
            "gha": {
                "template_context": "fixtures/basic-backwards",
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
    # Send a POST request to the API
    response = client.post('/generate', json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 201
    mock_persistence_instance.persist.assert_called_once()
