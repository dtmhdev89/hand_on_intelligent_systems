from config.settings import env_settings
from google import genai
import base64


class GeminiModel:
    def __init__(self) -> None:
        self.model_name_for_text = "gemini-2.0-flash"
        self.model_name_for_image = "gemini-2.0-flash-exp-image-generation"
        self._client = None
        self.generate_text_content_config = genai.types.GenerateContentConfig(
            # system_instruction=
            # temperature=
            max_output_tokens=100
        )
        self.generate_image_config = genai.types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )

    def client(self):
        """Instantiate google genai client"""

        if self._client is None:
            self._client = genai.Client(api_key=env_settings.GOOGLE_API_KEY)

        return self._client

    def text_generation(self, prompt) -> str:
        """Text Generation"""

        try:
            response = self.client().models.generate_content(
                model=self.model_name_for_text,
                contents=[prompt],
                config=self.generate_text_content_config
            )

            return response.text
        except Exception as e:
            print(str(e))
            raise

    def image_generation(self, prompt):
        """Image generation"""

        try:
            response = self.client().models.generate_content(
                model=self.model_name_for_image,
                contents=[prompt],
                config=self.generate_image_config
            )

            return GeminiModel.filter_out_images(response)
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def filter_out_images(response):
        """Filter out images from response and encode them as base64"""

        images = []

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                base64_encoded = base64.b64encode(part.inline_data.data).\
                                        decode('utf-8')
                data_url = f"data:image/png;base64,{base64_encoded}"
                images.append(data_url)
        
        return images
