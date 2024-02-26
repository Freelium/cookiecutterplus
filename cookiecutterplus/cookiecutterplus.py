from cookiecutter.main import cookiecutter
from cookiecutter.repository import determine_repo_dir
import tempfile, os, subprocess


class CookieCutterPlus:
    def __init__(self, state):
        self.state = state
        self.github_repo_prefix = f"https://github.com/{state.get('template_repo')}.git"
        self.authenticate_github_cli()

    def authenticate_github_cli(self):
        gh_token = os.environ.get('GITHUB_TOKEN')
        if gh_token is None:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        subprocess.run(["gh", "auth", "login", "--with-token"], input=gh_token.encode())
    
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
