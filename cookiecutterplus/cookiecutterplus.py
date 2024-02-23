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
            print(f"Applying template:{template} with context_vars:{template_values}")
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

def cli(args=None):
    import argparse
    parser = argparse.ArgumentParser(description='CookiecutterPlus CLI')
    parser.add_argument('-a', '--api-mode', type=bool, help='Run CookieCutterPlus in API Mode')
    parser.add_argument('-t', '--template_repo', type=str, help='The template repo to use')
    parser.add_argument('-p', '--payload', type=dict, help='The payload to use')
    parser.add_argument('-o', '--output_path', type=str, help='The output path to use')
    parser.add_argument('-n', '--no_input', type=bool, help='If enabled, you will be prompted for variable input.')
    args = parser.parse_args(args)
    # if args.api_mode is enabled then run the API, else instantiate CookieCutterPlus
    if args.api_mode:
        from api.app import CookieCutterPlusAPI
        ccp_api = CookieCutterPlusAPI()
        ccp_api.run()
    else:
        ccp = CookieCutterPlus(args.template_repo, args.payload, args.output_path, args.no_input)
        ccp.run()
