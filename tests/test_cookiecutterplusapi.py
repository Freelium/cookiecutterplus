import json, yaml, pytest, requests
from unittest.mock import patch, MagicMock
from api import CookieCutterPlusAPI


@pytest.fixture
def client():
   api = CookieCutterPlusAPI()
   app = api.get_flask_app()
   app.config['TESTING'] = True
   with app.test_client() as client:
       yield client 


def test_cookiecutter_api_success(tmp_path, client):
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
        "output_path": tmp_path,
        "no_input": True
    }
    # Send a POST request to the API
    response = client.post('/generate', json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 201


def test_cookiecutter_api_invalid_parameter(tmp_path, client):
    api = CookieCutterPlusAPI()
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
        "ccplus": {
            "badParameter": "badValue"
        },
        "output_path": tmp_path,
        "no_input": True
    }
    # Send a POST request to the API
    response = client.post('/generate', json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 400
