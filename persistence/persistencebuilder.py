from githubpersister import GitHubPersister
from localpersister import LocalPersister


class PersistenceBuilder:
    @staticmethod
    def get_persister(persistence_type):
        if persistence_type == 'local':
            return LocalPersister()
        if persistence_type == 'git':
            return GitHubPersister()
        else:
            raise ValueError(f"Type: {persistence_type} is unsupported")
