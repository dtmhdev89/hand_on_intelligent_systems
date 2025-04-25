from simple_ai_text_image_prompt_app.providers.openai.gpt_model import GPTModel
from simple_ai_text_image_prompt_app.providers.google.gemini_model import GeminiModel


class AIProvider:
    def __init__(self, provider: str) -> None:
        self.provider = provider

    def factory_model(self):
        if self.provider == "openai":
            return GPTModel()
        elif self.provider == "google-gemini":
            return GeminiModel()
