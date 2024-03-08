from persistence import PersistenceBuilder, GithubPersistence
import pytest


def test_persistence_factory_github():
    persistence = PersistenceBuilder.get_persister('gh')
    assert isinstance(persistence, GithubPersistence)
