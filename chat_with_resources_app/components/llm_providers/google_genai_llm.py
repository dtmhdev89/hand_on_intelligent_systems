import os
from langchain_google_genai import GoogleGenerativeAI


class GoogleGenaiLlm:
    """Openai LLM from langchain"""

    def __init__(self) -> None:
        self.__api_key_name = "GOOGLE_API_KEY"
        self._llm = None
        self._cb = None
        self._input_and_set_api_key()

    def _input_and_set_api_key(self):
        """Input api key if not set"""

        api_key_env = os.environ.get(self.__api_key_name, None)

        if api_key_env is not None:
            self.__api_key = os.environ[self.__api_key_name]
        else:
            self.__api_key = input("Enter Your Openai API Key:")
            os.environ[self.__api_key_name] = self.__api_key

    @property
    def llm(self):
        """_llm getter"""

        if self._llm is None:
            self._llm = GoogleGenerativeAI(model="gemini-2.0-flash")
        
        return self._llm

    @property
    def fn_callback(self):
        """_cb getter"""
        
        return self._cb
