from config.settings import env_settings
from google import genai


class GeminiModel:
    def __init__(self) -> None:
        self.model_name = "gemini-2.0-flash"
        self._client = None
        self.generate_content_config = genai.types.GenerateContentConfig(
            # system_instruction=
            # temperature=
            max_output_tokens=100
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
                model=self.model_name,
                contents=[prompt],
                config=self.generate_content_config
            )

            return response.text
        except Exception as e:
            return str(e)
