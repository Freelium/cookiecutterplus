from abc import ABC, abstractmethod


class TemplatePersister(ABC):

    @abstractmethod
    def persist(self, output_path, destination):
        pass
