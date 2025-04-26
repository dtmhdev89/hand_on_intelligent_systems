from typing import Literal, TypeAlias
from chat_with_resources_app.components.llm_providers.openai_llm import OpenaiLlm
from chat_with_resources_app.components.llm_providers.google_genai_llm import GoogleGenaiLlm

class LlmProvider:

    SupportedAIProvider: TypeAlias = Literal[
        "openai",
        "google-genai"
    ]

    def __init__(self, provider: SupportedAIProvider) -> None:
        self.provider = provider

    def factory_provider(self):
        """Create llm provider instance"""
        
        if self.provider == "openai":
            return OpenaiLlm()
        elif self.provider == "google-genai":
            return GoogleGenaiLlm()
