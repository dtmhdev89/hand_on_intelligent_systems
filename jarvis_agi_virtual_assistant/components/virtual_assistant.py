import os
import pyttsx3 as tts
import speech_recognition as sr
from google import genai


class VirtualAssistant:
    """Virtual Assistant"""

    def __init__(self) -> None:
        self.__tts_engine = tts.init()
        self.__recognizer = sr.Recognizer()
        self.__genai_client = None

    @property
    def tts_engine(self):
        """__tts_engine getter"""

        return self.__tts_engine
    
    @property
    def recognizer(self):
        """__recognizer getter"""

        return self.__recognizer
    
    @property
    def genai_client(self):
        """GenAI client"""

        if self.__genai_client is None:
            self.__genai_client = genai.Client(
                api_key=os.environ.get("GOOGLE_API_KEY")
            )

        return self.__genai_client
    
    def get_tts_engine_config(self):
        """Get TTS Engine configurations"""

        print("------TTS Engine Config: ")
        print("Rate: ", self.tts_engine.getProperty('rate'))

    def change_tts_engine_config(self):
        """Make change to tts engine config for more control"""

        # voices = self.tts_engine.getProperty("voices")
        # propose set vietnamese voice
        # self.tts_engine.setProperty('voice', voices[73].id)
        self.tts_engine.setProperty('rate', 150)

    def speak(self, text):
        """Speak action"""

        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def task_command(self):
        """Recognize command/prompt from user's microphone"""

        with sr.Microphone() as source:
            print("---Listening.....")
            # listen for 1 second of user's speech
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("-Recognizing.......")
            query = self.recognizer.recognize_google(audio, language="en-US")
            print("User said: " + query)
        except Exception as e:
            print(e)
            self.speak("Say that again please...")

            return None

        return query

    def generate_content(self, prompt):
        """Generate content from prompt"""

        try:
            response = self.genai_client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0,
                    top_p=0.95,
                    top_k=20,
                    candidate_count=1,
                    seed=5,
                    max_output_tokens=100,
                    stop_sequences=['STOP!'],
                    presence_penalty=0.0,
                    frequency_penalty=0.0,
                )
            )

            return response.text
        except Exception as e:
            print(e)
            raise

    def start(self):
        """Start virtual assistant"""

        self.change_tts_engine_config()
        self.get_tts_engine_config()
        query = None
        count = 1

        while (not query) and (count < 3):
            count += 1
            query = self.task_command()
            text_response = self.generate_content(prompt=query)
            self.speak(text=text_response)
