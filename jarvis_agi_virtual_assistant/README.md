# J.A.V.I.S AI assistant:
## Description:
- A voice AI assistant
- Use voice to make conversation with J.A.V.I.S
- No GUI at the moment

## Genai model:
- gemini-2.0-flash-001 model
- It will cost you when calling api to the model. NOT FREE, but at efficient cost. 

## How to run in local:

```
# setup must-have libs

brew install portaudio # if macos

# same lib for other OS
```

```
cd jarvis_agi_virtual_assistant
```

```
# create
pip install virtualenv # if not installed yet

python3 -m virtualenv .venv
```

```
# Activate virtual environment

source .venv/bin/activate
```

```
# environment variables
# .env
GOOGLE_API_KEY=
OPENWEATHERMAP_API_KEY=

# OPENWEATHERMAP_API_KEY for weather tool when request for weather
```

```
# install requirements.txt

pip install -r requirements.txt -q
```

```
# run app

python3 -m application
```

**Enjoy**

## More info:
### pyttsx3:
- it is just an interface
- the voice supported will relies on the underlying speech synthesis engines available on your operating system
