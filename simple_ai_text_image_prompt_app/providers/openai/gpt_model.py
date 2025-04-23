from config.settings import env_settings
from openai import OpenAI, RateLimitError


class GPTModel:
    def __init__(self) -> None:
        self.model_name = "gpt-3.5-turbo"
        self._client = None

    def client(self):
        """OpenAI client instance"""

        if self._client is None:
            self._client = OpenAI(api_key=env_settings.OPENAI_API_KEY)
        
        return self._client

    def text_generation(self, prompt):
        """Text generation"""
        try:
            response = self.client().responses.create(
                model=self.model_name,
                input=prompt
            )
            return response.output_text
        except RateLimitError as e:
            return str(e)
        except Exception as e:
            return str(e)

