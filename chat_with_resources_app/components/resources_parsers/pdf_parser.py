from PyPDF2 import PdfReader


class PdfParser:
    """PDF Parser"""

    def __init__(self, pdf_file):
        self._pdf_file = pdf_file
        self._reader = None

    @property
    def reader(self):
        """_reader getter"""

        if self._reader is None:
            self._reader = PdfReader(self._pdf_file)

        return self._reader

    def extract_text(self):
        """Make text extraction"""

        text = ""

        for page in self.reader.pages:
            text += page.extract_text()

        return text
