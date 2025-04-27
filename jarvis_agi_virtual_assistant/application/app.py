import pyttsx3 as tts
import speech_recognition as sr


class VirtualAssistant:
    """Virtual Assistant"""

    def __init__(self) -> None:
        self.__tts_engine = tts.init()
        self.__recognizer = sr.Recognizer()

    @property
    def tts_engine(self):
        """__tts_engine getter"""

        return self.__tts_engine
    
    @property
    def recognizer(self):
        """__recognizer getter"""

        return self.__recognizer

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
            query = self.recognizer.recognize_google(audio, language="")
        except Exception as e:
            print(e)
            print("---Please speak again.")
