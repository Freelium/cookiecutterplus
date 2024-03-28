from api.schema import MainSchema
import json

payload = '''{
  "output_path": "meep",
  "template_payloads": [
    {
      "template_context": "Tealium/tealium-cookiecutter",
      "template_path": "cookiecutter/shared/cookiecutter-gha",
      "context_vars": {
        "project_name": "my project"
      }
    }
  ]
}'''

def test_schema_validation():
    loaded = MainSchema().load(json.loads(payload))
    assert loaded['output_path'] == 'meep'
