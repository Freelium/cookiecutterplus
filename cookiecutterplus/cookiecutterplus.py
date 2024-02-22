from cookiecutter.main import cookiecutter
from cookiecutter.repository import determine_repo_dir
# from jsonschema import validate
# import json


class CookieCutterPlus:
    def __init__(self, template_repo, payload, output_path, no_input=True):
        self.github_repo_prefix = f"https://github.com/{template_repo}.git"
        self.payload = payload
        self.output_path = output_path
        self.no_input = no_input
        self.run()

    def run(self):
        for template, template_values in self.payload.items():
            print(f"On {template} with values {template_values}")
            cookiecutter(
                template=determine_repo_dir(template=self.github_repo_prefix,
                                            directory=template_values["template_path"],
                                            checkout="main",
                                            clone_to_dir="./template_repo",
                                            no_input=self.no_input,
                                            abbreviations="gh")[0],
                no_input=self.no_input,
                overwrite_if_exists=True,
                extra_context=template_values["context_vars"],
                output_dir=self.output_path
            )




# class CookieCutterPlus:
#     def __init__(self, template_input, output_path, no_input=True):
#         self.template_json_schema = {
#             "type": "object",
#             "properties": {
#                 "template": {
#                     "type": "object",
#                     "context_vars": {
#                         "type": "object",
#                     }
#                 },
#             },
#         }
#         self.template_map = template_input
#         self.output_path = output_path
#         self.no_input = no_input
#         self.run()
#
#     def run(self):
#         # First validate the input against the schema << is this necessary??????
#         if self.valid_schema():
#             # if the schema is valid, loop through template k/v and apply them
#             for template_path, values in self.template_map.items():
#                 self.apply_template(template_path, values["context_vars"])
#         print(f"Successfully templated: ${self.template_map}")
#
#     def valid_schema(self):
#         try:
#             print(f"Validating JSON Map against Schema: ${self.template_map}")
#             validate(self.template_map, schema=self.template_json_schema)
#             print(f"JSON Map is Valid, continuing: ${self.template_map}")
#             return True
#         except Exception as e:
#             print(f"${e}")
#
#     def apply_template(self, template, context):
#         """
#         Run Cookiecutter just as if using it from the command line.
#
#         :param template: A directory containing a project template directory,
#             or a URL to a git repository.
#         :param checkout: The branch, tag or commit ID to checkout after clone.
#         :param no_input: Do not prompt for user input.
#             Use default values for template parameters taken from `cookiecutter.json`, user
#             config and `extra_dict`. Force a refresh of cached resources.
#         :param extra_context: A dictionary of context that overrides default
#             and user configuration.
#         :param replay: Do not prompt for input, instead read from saved json. If
#             ``True`` read from the ``replay_dir``.
#             if it exists
#         :param overwrite_if_exists: Overwrite the contents of the output directory
#             if it exists.
#         :param output_dir: Where to output the generated project dir into.
#         :param config_file: User configuration file path.
#         :param default_config: Use default values rather than a config file.
#         :param password: The password to use when extracting the repository.
#         :param directory: Relative path to a cookiecutter template in a repository.
#         :param skip_if_file_exists: Skip the files in the corresponding directories
#             if they already exist.
#         :param accept_hooks: Accept pre and post hooks if set to `True`.
#         :param keep_project_on_failure: If `True` keep generated project directory even when
#             generation fails
#         """
#         print(f"Attempting to execute cookiecutter template: ${template} with context: ${context}")
#         try:
#             cookiecutter(
#                 template=template,
#                 no_input=self.no_input,
#                 extra_context=context,
#                 overwrite_if_exists=True,
#                 output_dir=self.output_path,
#             )
#             print(
#                 f"Successfully executed cookiecutter template: ${template}\n"
#                 f" with context: ${context}\n"
#                 f" to outputDir: ${self.output_path}")
#         except Exception as e:
#             print(f"${e}")


if __name__ == '__main__':
    template_map = {
        "cookiecutter-gha": {
            "template_path": "cookiecutter/shared/cookiecutter-gha",
            "context_vars": {
                "component_name": "test-component",
                "author": "Anonymous",
                "version": "0.1.0"
            },
        },
        "cookiecutter-java": {
            "template_path": "cookiecutter/shared/cookiecutter-java",
            "context_vars": {
                "component_name": "test-component",
                "author": "Anonymous",
                "jenkins_shared_lib_version": "7.5.6",
                "echo": "Hello, World!",
                "version": "0.1.0"
            }
        },
    }
    CookieCutterPlus(payload=template_map,
                     output_path="output/",
                     no_input=True)
