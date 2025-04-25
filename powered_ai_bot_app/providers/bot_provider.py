from powered_ai_bot_app.providers.telegram.interaction_bot import InteractionBot


class BotProvider:
    def __init__(self, bot_provider: str) -> None:
        self.bot_provider = bot_provider

    def factory_bot(self):
        if self.bot_provider == "telegram":
            return InteractionBot()
