from cookiecutter.main import cookiecutter
from cookiecutter.repository import determine_repo_dir
import tempfile
# from jsonschema import validate
# import json


class CookieCutterPlus:
    def __init__(self, state):
        self.state = state
        self.github_repo_prefix = f"https://github.com/{state.get('template_repo')}.git"

    def run(self):
        for template, template_values in self.state.get('payload').items():
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Applying template:{template} with context_vars:{template_values}")
                cookiecutter(
                    template=determine_repo_dir(template=self.github_repo_prefix,
                                                directory=template_values["template_path"],
                                                checkout="main",
                                                clone_to_dir=temp_dir,
                                                no_input=self.state.get('no_input'),
                                                abbreviations="gh")[0],
                    no_input=self.state.get('no_input'),
                    overwrite_if_exists=True,
                    extra_context=template_values["context_vars"],
                    output_dir=self.state.get('output_path')
                )
