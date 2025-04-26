from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Literal, TypeAlias
import os


class Embeddings:
    SUPPORTED_EMBEDDINDS = [
        "openai",
        "google-genai",
        "huggingface"
    ]

    SupportedEmbeddingsType: TypeAlias = Literal[
        "openai",
        "google-genai",
        "huggingface"
    ]
    
    def __init__(self, emb_type: SupportedEmbeddingsType) -> None:
        self.emb_type = emb_type
        self.validate_emb_type()
    
    def validate_emb_type(self):
        if self.emb_type not in self.__class__.SUPPORTED_EMBEDDINDS:
            raise ValueError(
                f"""Not supported embedding type
                Currently support:
                {" ".join(self.__class__.SUPPORTED_EMBEDDINDS)}
                """)
    
    def factory_embedding(self):
        if self.emb_type == "openai":
            return OpenAIEmbeddings()
        elif self.emb_type == "google-genai":
            return GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.environ.get("GOOGLE_API_KEY")
            )
        elif self.emb_type == "huggingface":
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )


