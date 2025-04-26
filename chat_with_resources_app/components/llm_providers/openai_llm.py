import os
from langchain_community.llms import openai
from langchain_community.callbacks import get_openai_callback


class OpenaiLlm:
    """Openai LLM from langchain"""

    def __init__(self) -> None:
        self.__api_key_name = "OPENAI_API_KEY"
        self._llm = None
        self._cb = get_openai_callback()
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
            self._llm = openai.OpenAI(api_key=self.__api_key,)
        
        return self._llm

    @property
    def fn_callback(self):
        """_cb getter"""
        
        return self._cb
