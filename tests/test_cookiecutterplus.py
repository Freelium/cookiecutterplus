import yaml
from cookiecutterplus import CookieCutterPlus

def test_cookiecutter_basic_backwards_compat(tmp_path):
    test_payload = {
        "output_path": tmp_path,
        "payload": {
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
        "payload": {
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
