from pathlib import Path
from cookiecutterplus import CookieCutterPlusSkinny


def test_cookiecutter_plus_skinny_runs(tmp_path):
    # Define your test payload and output path
    test_payload = {
        "template1": {
            "template_path": "cookiecutter/shared/cookiecutter-gha",
            "context_vars": {"key1": "value1", "key2": "value2"}
        }
    }
    test_output_path = Path(tmp_path, 'test/output/path')

    # Instantiate and run your class
    ccp = CookieCutterPlusSkinny(payload=test_payload, output_path=test_output_path)
    ccp.run()
