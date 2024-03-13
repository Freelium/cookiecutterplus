from .githubpersistence import GithubPersistence


class PersistenceBuilder:
    @staticmethod
    def get_persister(persistence_type):
        if persistence_type == 'gh':
            return GithubPersistence()
        else:
            raise ValueError(f"Type: {persistence_type} is unsupported")
