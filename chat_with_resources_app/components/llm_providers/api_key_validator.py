import os
import streamlit as st


class ApiKeyValidator:
    """API Key Validator"""

    AI_PROVIDER_ENV_KEY = {
        "google-genai": "GOOGLE_API_KEY",
        "openai": "OPENAI_API_KEY"
    }

    def __init__(self, ai_provider: str) -> None:
        self.ai_provider = ai_provider
    
    def validate_and_input(self):
        """Check and setup input api key"""

        api_key_env = os.environ.get(
            ApiKeyValidator.AI_PROVIDER_ENV_KEY[self.ai_provider],
            None
        )

        if api_key_env is None:
            api_key = None

            api_key = st.text_input(
                f"Enter Your {self.ai_provider} API Key:",
                type="password",
                key=f"api_key_input_{self.ai_provider}"
            )
            
            if st.button("Set", key=f"api_key_btn_{self.ai_provider}"):
                if api_key:
                    os.environ[
                        ApiKeyValidator.AI_PROVIDER_ENV_KEY[self.ai_provider]
                    ] = api_key
                    st.success("API Key Set!")
                    st.rerun()  # Rerun to update the UI
                else:
                    st.error("Please enter your API Key.")
