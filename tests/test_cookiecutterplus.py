import yaml, pytest, requests
from jsonschema import ValidationError
from cookiecutterplus import CookieCutterPlus
from api import CookieCutterPlusAPI

@pytest.fixture
def api_url():
    return 'http://localhost:5000/generate'

# def test_cookiecutter_basic_persistence_github(tmp_path):
#     test_payload = {
#         "output_path": tmp_path,
#         "payload": {
#             "gha": {
#                 "template_context": "tests/fixtures/basic-backwards",
#                 "template_path": "",
#                 "context_vars": {
#                     "component_name": "My Cut Cookie",
#                     "project_name": "my-cut-cookie",
#                     "project_slug": "my-cut-cookie"
#                 }
#             }
#         },
#         "persistence": {
#             "github": {
#                 "destination": "my-org/my-repo",
#                 "repo_type": "public"
#             }
#         },
#         "no_input": True
#     }

#     # Instantiate and run your class
#     ccp = CookieCutterPlus(test_payload)
#     ccp.run()

#     dir = tmp_path / "my-cut-cookie"
#     simple_yaml_file = dir / "simple.yaml"

#     assert dir.is_dir()
#     assert simple_yaml_file.is_file()
#     with open(simple_yaml_file) as f:
#         data = yaml.safe_load(f)
#         assert data == {"name": "my-cut-cookie"}

def test_cookiecutter_api(tmp_path):
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
        "no_input": True1  
    }
    # Send a POST request to the API
    response = requests.post(api_url, json=cookiecutterplus_payload)
    # Assert the response status code is 201
    assert response.status_code == 201
    # Assert the response message is 'CookieCutter generation completed successfully'
    assert response.json()['message'] == 'CookieCutter generation completed successfully'




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
