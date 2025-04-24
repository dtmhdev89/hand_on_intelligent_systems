import streamlit as st
import sys
import os

up_levels = [".."] * 1
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    *up_levels
))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from providers.provider import AIProvider


class StreamlitApp:
    """Streamlit App"""
    def __init__(self, provider="google-gemini"):
        self.provider = provider
        self.provider_name = provider.replace("-", " ").capitalize()
        self.genai_model = AIProvider(provider=provider).factory_model()

    def _gui(self):
        """GUI for streamlit app"""

        st.title(f"{self.provider_name} Powererd Text To Image Generation")
        prompt = st.text_area(
            "Enter a prompt to generate a Image"
        )
        size_options = [
            "256x256",
            "512x512",
            "1024x1024"
        ]
        selected_size = st.selectbox("Select image's size", size_options)
        if st.button("Generate"):
            try:
                image_responses = self.genai_model.image_generation(
                    prompt=StreamlitApp.prompt_construction(
                        prompt=prompt,
                        selected_size=selected_size
                    )
                )

                if image_responses:
                    for b64_img in image_responses:
                        st.image(b64_img, use_container_width=True)
                        href = f'<a class="download-button" href="{b64_img}" '\
                            'download="generated_image.png">'\
                            'Download</a>'
                        st.markdown(href, unsafe_allow_html=True)
                else:
                    st.warning("No image generated")
            except Exception as e:
                print(str(e))
                st.error(e)
    
    def run(self):
        """Run GUI streamlit app"""

        self._gui()

    @staticmethod
    def prompt_construction(prompt, selected_size, number_of_images=1):
        """Construct prompt following a format"""

        prompt = f"""
        Generate {number_of_images} image that has size of ({selected_size})
        by below description:
        {prompt}
        """

        return prompt


if __name__ == "__main__":
    StreamlitApp().run()
