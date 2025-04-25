# Powered AI Bot App
## Description:
Bot app server that powered AI for a bot service like Telegram,...

## Supported bot service:
- Telegram
- Others in the future

## Supported AI sdk:
- Google gemini  # since it has a great free quota for personal use
- Future: openai, claude, so on.

## Why running with FastAPI:
- The first reason, the bot app need to be run in a loop like pooling mechanism to listen response from the bot service.
- The second reason, the asynchronous mechanism helps the bot app hanles multple msg request at a time, so that it's more flexible than runs in synchronous mechanism

FastAPI could handle both with lifespan to run bot loop runner in block way in each thread but aschronous way for the bot app.

Running in lifespan so we don't need to define any router to run FastAPI app since we don't need it.

With lifespan we can handle startup and shutdown efficiently to manage the bot app server.

## How to run the bot app server:
### Environment settings:
```
cd powered_ai_bot_app
```

```
# create .env file in the directory powered_ai_bot_app
# or could be somewhere else in your system
# the must have environment keys for the bot app to run

APP_ENV=development  # or any environment
TELEGRAM_API_KEY=
TELEGRAM_BOT_USERNAME=
GOOGLE_API_KEY=
OPENAI_API_KEY=

# Let OPENAI_API_KEY be empty since the bot app doesn't support openai at the moment
# Ref: https://telepot.readthedocs.io/en/latest/#id5 to setup and get TELEGRAM_API_KEY and TELEGRAM_BOT_USERNAME
# Ref: https://ai.google.dev/gemini-api/docs/api-key to setup and get GOOGLE_API_KEY
```

```
export ENV_FILE_PATH=<path_to_your_.env>
```

### With only Uvicorn:

- Not the best way, but like a comparison with fastAPI and Uvicorn way below

```
cd powered_ai_bot_app
```

```
uvicorn application.async_app:app --log-config config/logging_config.yaml
```

### With Uvicorn in FastAPI server:

```
cd powered_ai_bot_app
```

```
uvicorn application.fastapi_app:app --log-config config/logging_config.yaml
```

## Let's have a fun with your own bot app
