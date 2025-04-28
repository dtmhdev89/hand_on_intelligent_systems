import os
import pyttsx3 as tts
import speech_recognition as sr
from google import genai
import requests
import json
import time


class VirtualAssistant:
    """Virtual Assistant"""

    def __init__(self) -> None:
        self.__tts_engine = tts.init()
        self.__recognizer = sr.Recognizer()
        self.__genai_client = None
        self.is_running = True

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

    def task_command(self, wait_for_activation=False):
        """Recognize command/prompt from user's microphone"""

        with sr.Microphone() as source:
            print("---Listening.....")
            # listen for 1 second of user's speech
            self.recognizer.pause_threshold = 1.5
            audio = self.recognizer.listen(source)

        try:
            print("-Recognizing.......")
            query = self.recognizer.recognize_google(audio, language="en-US")
            print("User said: " + query)
        except Exception as e:
            print(e)
            if not wait_for_activation:
                self.speak("Say that again please...")

            return None

        return query
    
    def _generation_configs(self, tools: list | None = []):
        """Generation configs for genai"""

        base_configs = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 20,
            "candidate_count": 1,
            "seed": 5,
            "max_output_tokens": 200,
            "stop_sequences": ['STOP!'],
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0
        }

        configs = genai.types.GenerateContentConfig(
            **base_configs,
            tools=tools
        )

        return configs

    def tools_functions(self):
        """Define functions for tools of genai"""

        handle_goodbye_fn = genai.types.FunctionDeclaration(
            name='handle_goodbye',
            description="Terminates the program.",
            parameters=genai.types.Schema(
                type='OBJECT',
                properties={}
            )
        )

        get_weather_fn = genai.types.FunctionDeclaration(
            name='get_weather',
            description="Gets the current weather for a location.",
            parameters=genai.types.Schema(
                type='OBJECT',
                properties={
                    'location': genai.types.Schema(
                        type='STRING',
                        description="The city and state (e.g., 'Los Angeles, CA')"
                    )
                },
                required=['location']
            )
        )

        return (handle_goodbye_fn, get_weather_fn)

    def generate_content(self, prompt, with_tools=True):
        """Generate content from prompt"""

        if with_tools:
            tools = genai.types.Tool(
                function_declarations=[*self.tools_functions()]
            )
            try:
                response = self.genai_client.models.generate_content(
                    model='gemini-2.0-flash-001',
                    contents=prompt,
                    config=self._generation_configs(
                        tools=[tools]
                    )
                )
                return response
            except Exception as e:
                print(e)
                raise
        else:
            try:
                response = self.genai_client.models.generate_content(
                    model='gemini-2.0-flash-001',
                    contents=prompt,
                    config=self._generation_configs(),
                )
                return response.text
            except Exception as e:
                print(e)
                raise

    def handle_goodbye(self):
        """Handle the goodbye action."""

        self.speak("...Goodbye!...")
        time.sleep(1)
        self.is_running = False

    def get_weather(self, location):
        """
        Gets the weather for a specified location using OpenWeatherMap API.
        """

        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": os.environ.get("OPENWEATHERMAP_API_KEY"),
            "units": "metric",  # Get temperature in Celsius
        }

        try:
            response = requests.get(
                base_url,
                params=params,
                timeout=500
            )
            response.raise_for_status()
            weather_data = response.json()
            print(f"OpenWeatherMap API response: {weather_data}")
            # Extract relevant information
            temperature = weather_data["main"]["temp"]
            condition = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]
            weather_info = {
                "temperature": temperature,
                "condition": condition,
                "humidity": humidity
            }

            return json.dumps(weather_info)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            self.speak(f"Sorry, I could not retrieve the weather for {location}.")
            return json.dumps({"error": str(e)})
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            self.speak(f"Sorry, I could not understand the weather data for {location}.")
            return json.dumps({"error": "Error parsing weather data."})

    def start(self):
        """Start virtual assistant"""

        self.change_tts_engine_config()
        self.get_tts_engine_config()

        wait_for_activation = True

        while wait_for_activation:
            query = self.task_command(wait_for_activation=wait_for_activation)
            if query and query.strip().lower() == "hi jarvis":
                wait_for_activation = False

        self.speak("Hi, I'm JARVIS, your virtual assistant!")
        time.sleep(1)

        next_command = False

        while self.is_running:
            if next_command:
                self.speak("Tell me next command or goodbye for termination...")

            query = self.task_command()
            if query:
                next_command = True

                response = self.generate_content(
                    prompt=query
                )

                if response.function_calls:
                        for fn_call in response.function_calls:
                            if fn_call.name == "handle_goodbye":
                                self.handle_goodbye()
                            elif fn_call.name == "get_weather":
                                fn_call_args = fn_call.args
                                location = fn_call_args.get("location", None)
                                if location:
                                    weather_data_json = self.get_weather(location=location)
                                    weather_data = json.loads(weather_data_json) #load json
                                    if "error" not in weather_data:
                                        temperature = weather_data["temperature"]
                                        condition = weather_data["condition"]
                                        humidity = weather_data["humidity"]
                                        self.speak(f"The weather in {location} is {condition} with a temperature of {temperature} degrees Celsius and {humidity}% humidity.")
                                    else:
                                        self.speak(f"Sorry, there was an error getting the weather in {location}")

                                else:
                                    print("--No extracted location")
                            else:
                                self.speak("I can't do that yet.")
                else:
                    text_response = response.text
                    next_command = False
                    self.speak(text=text_response)
            else:
                self.speak("Sorry, I could not understand you.")
