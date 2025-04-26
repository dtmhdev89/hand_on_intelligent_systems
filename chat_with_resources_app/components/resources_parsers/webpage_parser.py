from langchain_community.document_loaders import WebBaseLoader


class WebpageParser:
    """Webpage Parser"""

    def __init__(self, url: str) -> None:
        self.url = url
        self._reader = None

    @property
    def reader(self):
        """_reader getter"""

        if self._reader is None:
            self._reader = WebBaseLoader(self.url)

        return self._reader

    def extract_text(self):
        """Make text extraction"""

        docs = self.reader.load()
        text = "\n".join([document.page_content for document in docs])
        
        return text
