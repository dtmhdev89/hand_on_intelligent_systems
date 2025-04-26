from abc import ABC, abstractmethod


class BaseSearch(ABC):
    """Search Interface"""

    @abstractmethod
    def build_text_indexes(self, chunks):
        """Implement text indexes in subclass"""

    @abstractmethod
    def similarity_search(self, query):
        """Implement similarity search"""
