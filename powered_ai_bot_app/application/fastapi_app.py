from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from powered_ai_bot_app.application.app import BotApp

bot_app = BotApp(bot_provider="telegram")
background_task = None  # store the task

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler as context manager"""

    # Before functions
    global background_task
    print("-"*16)
    print("Running bot")
    loop = asyncio.get_running_loop()
    background_task = loop.run_in_executor(None, bot_app.run_loop)

    # This is where the app runs
    yield

    # After functions
    print("Stop bot loop runner")
    bot_app.stop_loop()
    if background_task:
        await background_task  # wait for it to finish
    print("Shutting down")


app = FastAPI(lifespan=lifespan)
