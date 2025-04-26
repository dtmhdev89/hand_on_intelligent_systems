from PyPDF2 import PdfReader


class PdfParser:
    """PDF Parser"""

    def __init__(self, pdf_file):
        self._pdf_file = pdf_file
        self._pdf_reader = None
    
    @property
    def pdf_reader(self):
        if self._pdf_reader is None:
            self._pdf_reader = PdfReader(self._pdf_file)

        return self._pdf_reader

    def extract_text(self):
        """Make text extraction"""

        text = ""

        for page in self.pdf_reader.pages:
            text += page.extract_text()

        return text
