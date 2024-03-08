import yaml, pytest, requests
from unittest.mock import patch, MagicMock
from api import CookieCutterPlusAPI


@pytest.fixture
def api_url():
    return 'http://localhost:5000/generate'


def test_cookiecutter_api(tmp_path, api_url):
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
        "output_path": tmp_path,
        "no_input": True
    }
    # Send a POST request to the API
    response = requests.post(api_url, json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 201
    # Assert the response message is 'CookieCutter generation completed successfully'
    assert response.json()['message'] == 'CookieCutter generation completed successfully'


def test_cookiecutter_api_invalid_parameter(tmp_path, api_url):
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
    response = requests.post(api_url, json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 400
    # Assert the response message is 'CookieCutter generation completed successfully'
    assert response.json()['message'] == 'CookieCutter generation completed successfully'
