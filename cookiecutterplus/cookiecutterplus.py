from cookiecutter.main import cookiecutter
from cookiecutter.repository import determine_repo_dir, is_repo_url
from persistence.persistencebuilder import PersistenceBuilder
from jsonschema import validate
import json, os, subprocess, tempfile


class CookieCutterPlus:
    def __init__(self, state):
        self.state = state

    def run(self):
        # Iterate over the payload and apply the templates
        print(f"State {self.state.get('persistence').items()}")
        print(f"Payload {self.state.get('template_payload').items()}")
        for template, template_values in self.state.get('template_payload').items():
            print(f"Applying template:{template} with context_vars:{template_values}")
            # Use a temporary directory to clone the template repo
            with tempfile.TemporaryDirectory() as temp_dir:
                """.git/
                This method from the CookieCutter library will clone the templates, 
                    however it does have a dependency on Git or GH existing locally.
                """
                template = determine_repo_dir(template=template_values["template_context"],
                                              directory=template_values["template_path"],
                                              checkout="main",
                                              clone_to_dir=temp_dir,
                                              no_input=self.state.get('no_input'),
                                              abbreviations="gh")[0]
                # Evaluate the schema and patch the config
                CookieCutterPlus.evaluate_schema(template, template_values)
                print(f'run template values {template_values}')
                print(f'template_values["context_vars"] {template_values["context_vars"]}')
                cookiecutter(
                    template=template,
                    no_input=self.state.get('no_input'),
                    overwrite_if_exists=True,
                    extra_context=template_values["context_vars"],
                    output_dir=self.state.get('output_path'),
                )
        # If the persistence arg exists, run persist_output()
        if self.state.get('persistence'):
            self.persist_output()

    def persist_output(self):
        # Retrieve the persistence type and values from the state
        # key in the persistence dictionary == persistence type
        # values in the persistence dictionary == persistence values
        print(f"Persistence {self.state.get('persistence').items()}")
        for persistence_type, persistence_values in self.state.get('persistence').items():
            # Setup the persistence class using the factory
            persistence_class = PersistenceBuilder.get_persister(persistence_type)
            # Persist the output
            persistence_class.persist(f"{self.state.get('output_path')}/terraform-test-component",
                                      persistence_values["destination"])

    @staticmethod
    def evaluate_schema(template, template_values):
        ccplus_config_exists = os.path.isfile(
            os.path.join(template, 'ccplus.json')
        )
        if ccplus_config_exists:
            key = 'context_vars'
            CookieCutterPlus.validate_additive(template, template_values)
            context_vars = template_values.get(key, {})
            context_vars['ccplus'] = template_values.get('ccplus', {})

            if key not in template_values:
                template_values[key] = context_vars

        CookieCutterPlus.patch_config(template, template_values)

    @staticmethod
    def validate_additive(template, template_values):
        schema_path = os.path.join(template, 'ccplus.json')
        schema = CookieCutterPlus.load_schema(schema_path)
        data = template_values.get('ccplus', None)

        validate(instance=data, schema=schema)

    @staticmethod
    def load_schema(schema_path):
        with open(schema_path, 'r') as file:
            schema = json.load(file)
        return schema

    @staticmethod
    def patch_config(template, template_values):
        cookiecutter_path = os.path.join(template, 'cookiecutter.json')

        try:
            with open(cookiecutter_path, 'r') as cookiecutter_config:
                data = json.load(cookiecutter_config)
        except FileNotFoundError:
            data = {}

        data.update(template_values)

        with open(cookiecutter_path, 'w') as cookiecutter_config:
            json.dump(data, cookiecutter_config, indent=4)
