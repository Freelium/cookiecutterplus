from abc import ABC, abstractmethod


class TemplatePersister(ABC):

    @abstractmethod
    def persist(self, template, destination):
        pass
