from templatepersister import TemplatePersister
import os, subprocess


class LocalPersistence(TemplatePersister):
    def persist(self, template, destination):
        # persistence logic here
        print("Persisting to local dir")
