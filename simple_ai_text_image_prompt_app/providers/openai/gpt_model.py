from config.settings import env_settings
from openai import OpenAI, RateLimitError


class GPTModel:
    def __init__(self) -> None:
        self.model_name_for_text = "gpt-3.5-turbo"
        self.model_name_for_image = "dall-e-3"
        self.image_size = "1024x1024"
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
                model=self.model_name_for_text,
                input=prompt
            )
            return response.output_text
        except RateLimitError as e:
            print(str(e))
            raise
        except Exception as e:
            print(str(e))
            raise

    def image_generation(self, prompt):
        """Image generation"""

        try:
            response = self.client().images.generate(
                model=self.model_name_for_image,
                prompt=prompt,
                size=self.image_size,
                quality="standard",
                n=1
            )

            image_url = response.data[0].url

            return image_url
        except RateLimitError as e:
            print(str(e))
            raise
        except Exception as e:
            print(str(e))
            raise
