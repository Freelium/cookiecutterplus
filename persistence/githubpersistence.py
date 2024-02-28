from templatepersister import TemplatePersister
import os, subprocess


class GithubPersistence(TemplatePersister):
    def __init__(self):
        gh_token = os.environ.get('GITHUB_TOKEN')
        if gh_token is not None:
            subprocess.run(["gh", "auth", "login", "--with-token"], input=gh_token.encode())


    def persist(self, template, destination):
        # persistence logic goes here
        print("persisting template to github repo")