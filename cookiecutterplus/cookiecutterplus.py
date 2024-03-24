from cookiecutter.main import cookiecutter
from cookiecutter.repository import determine_repo_dir, is_repo_url
from .ccpexception import CookieCutterPlusError
from persistence.persistencebuilder import PersistenceBuilder
from jsonschema import validate, ValidationError
import json, os, subprocess, tempfile


class CookieCutterPlus:
    def __init__(self, state):
        self.state = state
        self.output_base = os.getenv('OUTPUT_BASE', '')

    def run(self):
        # Iterate over the payload and apply the templates
        for template_values in self.state.get('template_payloads'):
            print(f"Applying template: {template_values}")
            # Use a temporary directory to clone the template repo
            with tempfile.TemporaryDirectory() as temp_dir:
                """
                This determine_repo_dir method from the CookieCutter library will clone the templates, 
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
                cookiecutter(
                    template=template,
                    no_input=self.state.get('no_input'),
                    overwrite_if_exists=True,
                    extra_context=template_values["context_vars"],
                    output_dir=self.output_base,
                )
        # If the persistence arg exists, run persist_output()
        if self.state.get('persistence'):
            self.persist_output()

    def persist_output(self):
        # Retrieve the persistence type and values from the state
        # key in the persistence dictionary == persistence type
        # values in the persistence dictionary == persistence values
        for persistence_type, persistence_values in self.state.get('persistence').items():
            # Setup the persistence class using the factory
            persistence_class = PersistenceBuilder.get_persister(persistence_type)
            # Persist the output
            persistence_class.persist(f"{self.output_base}{self.state.get('output_path')}",
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
            context_vars.update(template_values.get('ccplus', {}))
            print(f"Updating {key} with {context_vars}")

            if key not in template_values:
                template_values[key] = context_vars
            print(f"Updated {key} with {context_vars}")
            print(f"Template values: {template_values}")

        CookieCutterPlus.patch_config(template, template_values)

    @staticmethod
    def validate_additive(template, template_values):
        config_path = os.path.join(template, 'ccplus.json')
        config = CookieCutterPlus.load_ccplus_config(config_path)
        schema = config.get('schema', dict())
        data = template_values.get('ccplus', None)
        print(f"Validating {data} against {schema}")

        try:
            validate(instance=data, schema=schema)
        except ValidationError as ex:
            raise CookieCutterPlusError('Issue validating cc+ additive') from ex

    @staticmethod
    def load_ccplus_config(config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config

    @staticmethod
    def patch_config(template, template_values):
        cookiecutter_path = os.path.join(template, 'cookiecutter.json')

        try:
            with open(cookiecutter_path, 'r') as cookiecutter_config:
                data = json.load(cookiecutter_config)
        except FileNotFoundError:
            data = {}

        # We want to favor the context_vars value should any overlap occur
        # but only if it's not None
        context_vars = template_values.get('context_vars', {})
        for key, value in context_vars.items():
            if value is not None:
                data[key] = value

        with open(cookiecutter_path, 'w') as cookiecutter_config:
            json.dump(data, cookiecutter_config, indent=4)
