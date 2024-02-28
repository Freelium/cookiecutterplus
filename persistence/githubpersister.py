from templatepersister import TemplatePersister
import os, subprocess


class GitHubPersister(TemplatePersister):
    def persist(self, template, destination):
        # persistence logic goes here
        print("persisting github template")