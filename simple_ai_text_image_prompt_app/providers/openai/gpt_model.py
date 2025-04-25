from simple_ai_text_image_prompt_app.config.settings import env_settings
from openai import OpenAI, RateLimitError
import base64


class GPTModel:
    def __init__(
        self,
        number_of_images: int | None = 1,
        image_size: str | None = "256x256"
    ) -> None:
        self.number_of_images = number_of_images
        self.image_size = image_size
        self.model_name_for_text = "gpt-3.5-turbo"
        self.model_name_for_image = "dall-e-3"
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
                response_format="b64_json",
                n=self.number_of_images
            )

            image_data = []
            for img in response.data:
                image_base64 = base64.b64decode(img.b64_json)
                base64_encoded = base64.b64encode(image_base64).decode('utf-8')
                data_url = f"data:image/png;base64,{base64_encoded}"
                image_data.append(data_url)

            return image_data
        except RateLimitError as e:
            print(str(e))
            raise
        except Exception as e:
            print(str(e))
            raise
