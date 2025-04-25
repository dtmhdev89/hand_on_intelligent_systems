# Running with uvicorn only

import asyncio
from powered_ai_bot_app.application.app import BotApp

bot_app = BotApp(bot_provider="telegram")


async def start_bot():
    """Start the bot in a background task"""

    print("-"*20)
    print("start_bot running")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, bot_app.run_loop)


async def app(scope, receive, send):
    """ASGI app — required by uvicorn"""

    if scope["type"] == "lifespan":
        print("-"*20)
        print("lifespan type running")
        await send({"type": "lifespan.startup.complete"})
        await start_bot()  # kick off bot on startup
        await send({"type": "lifespan.shutdown.complete"})
