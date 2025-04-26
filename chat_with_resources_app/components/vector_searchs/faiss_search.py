from langchain_community.vectorstores import faiss
from chat_with_resources_app.components.vector_searchs.base_search import BaseSearch


class FaissSearch(BaseSearch):
    def __init__(self, embeddings) -> None:
        self.__embeddings = embeddings

    @property
    def embeddings(self):
        return self.__embeddings

    def build_text_indexes(self, chunks):
        """Text Indexes"""

        self._search_index = faiss.FAISS.from_texts(chunks, self.__embeddings)

        return self._search_index

    def similarity_search(self, query):
        """Similarity Search"""

        return self._search_index.similarity_search(query)

