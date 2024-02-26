
from pathlib import Path
from cookiecutterplus import CookieCutterPlus

def test_cookiecutter_plus_runs(tmp_path):
    # Define your test payload and output path
    test_payload = {
        "template_repo": "Tealium/tealium-cookiecutter",
        "output_path": "meep",
        "payload": {
            "gha": {
                "template_path": "cookiecutter/shared/cookiecutter-gha",
                "context_vars": {
                    "blah": 123
                }
            }
        },
        "no_input": True
    }

    # Instantiate and run your class
    ccp = CookieCutterPlus(test_payload)
    ccp.run()
