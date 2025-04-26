from typing import Literal, TypeAlias
from chat_with_resources_app.components.vector_searchs.faiss_search import FaissSearch


class VectorSearch:
    """Vector Search"""

    SUPPORTED_ALGORITHMS = [
        "faiss"
    ]

    SupportedSearchAlgorithm: TypeAlias = Literal[
        "faiss"
    ]

    def __init__(
            self,
            search_algorithm: SupportedSearchAlgorithm,
            embeddings
        ) -> None:
        self.search_algorithm = search_algorithm
        self.embeddings = embeddings
        self._validate_supported()

    def _validate_supported(self):
        """search_algorithm validation"""

        if self.search_algorithm not in self.__class__.SUPPORTED_ALGORITHMS:
            raise ValueError("Not supported algorithms")

    def factory_search(self):
        """Create search instance"""

        if self.search_algorithm == "faiss":
            return FaissSearch(
                embeddings=self.embeddings
            )
