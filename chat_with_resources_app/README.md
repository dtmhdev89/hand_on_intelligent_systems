# Chat With Resource App
## Description:
- Do question-awnser task with the resource;
- Currently support chat with PDF and a webpage
## Tech stack:
- Using RAG with LLMs like openai or google gemini flash to construct the question-answer task;
- Using langchain to implement;
- Using streamlit for demo deployment;
## How to run it in local:
### Environment settings:
```
cd chat_with_resources_app
```

```
# create .env file in the directory powered_ai_bot_app
# or could be somewhere else in your system
# the must have environment keys for the bot app to run

APP_ENV=development  # or any environment
GOOGLE_API_KEY=
OPENAI_API_KEY=

# [Optional] OPENAI_API_KEY
# [Optional] GOOGLE_API_KEY --> Ref: https://ai.google.dev/gemini-api/docs/api-key to setup and get
```

```
# install virtualenv if not installed yet
pip install virtualenv
```

```
# create virtual environment
# cd chat_with_resources_app  # if not

python3 -m virtualenv .venv

source .venv/bin/activate
```

```
# install libs
pip install -r requirements.txt -q
```

```
# Export ENV_FILE_PATH
export ENV_FILE_PATH=<path_to_your_.env>
```

### Start local streamlit server:
```
# cd chat_with_resources_app  # if not

python3 -m streamlit run application/streamlit_app.py

# or

streamlit run application/streamlit_app.py
```

### Enjoy your app.
