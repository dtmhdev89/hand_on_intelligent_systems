import time
from powered_ai_bot_app.providers.bot_provider import BotProvider


class BotApp:
    """Powered AI Bot App"""

    def __init__(self, bot_provider: str) -> None:
        self.bot_provider = bot_provider
        self._bot_runner = None
        self._interval_time = 20  # seconds
        self._should_run = True  # to control loop

    @property
    def bot_runner(self):
        """Bot instance instantiation"""

        if self._bot_runner is None:
            self._bot_runner = BotProvider(
                bot_provider=self.bot_provider
            ).factory_bot()

        return self._bot_runner

    def run_loop(self):
        """Loop runner"""

        self.bot_runner.run_loop()
        while self._should_run:
            time.sleep(self._interval_time)

    def stop_loop(self):
        """Stop loop runner"""

        self._should_run = False
