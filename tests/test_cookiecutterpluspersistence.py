from persistence import PersistenceBuilder, GithubPersistence
import pytest

# Test the PersistenceBuilder factory returns the GitHub persistence class
def test_persistence_factory_github():
    persistence = PersistenceBuilder.get_persister('gh')
    assert isinstance(persistence, GithubPersistence)
