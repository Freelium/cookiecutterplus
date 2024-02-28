from githubpersister import GithubPersistence
from localpersister import LocalPersistence


class PersistenceBuilder:
    @staticmethod
    def get_persister(persistence_type):
        if persistence_type == 'local':
            return LocalPersistence()
        if persistence_type == 'git':
            return GithubPersistence()
        else:
            raise ValueError(f"Type: {persistence_type} is unsupported")
