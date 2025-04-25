from simple_ai_text_image_prompt_app.providers.provider import AIProvider
from powered_ai_bot_app.config.settings import env_settings
import telepot
from telepot.loop import MessageLoop


class InteractionBot:
    def __init__(self) -> None:
        self._bot = None

    @property
    def bot(self):
        """Bot memoized instance"""

        if self._bot is None:
            self._bot = telepot.Bot(env_settings.TELEGRAM_API_KEY)

        return self._bot

    def _handler(self, msg):
        """Telegram bot handler"""

        user_name = " ".join(
            [
                msg['from']['first_name'],
                msg['from']['last_name']
            ]
        )

        content_type, _chat_type, chat_id = telepot.glance(msg)

        if (content_type == "text"):
            command = msg['text']

            if 'hello' in command.split()[:2]:
                self.bot.sendMessage(
                    chat_id,
                    f"hello this is telebot, {user_name}"
                )
            elif 'bye' in command.split()[:2]:
                self.bot.sendMessage(
                    chat_id,
                    f"Bye there, {user_name}"
                )
            elif ('thank you' in command.split()[:4]) or ('thanks' in command.split()[:4]):
                self.bot.sendMessage(
                    chat_id,
                    f"You're welcome, {user_name}"
                )
            else:
                genai_model = AIProvider(
                    provider="google-gemini"
                ).factory_model()
                text_response = genai_model.text_generation(prompt=command)

                self.bot.sendMessage(
                    chat_id,
                    text_response
                )

    def run_loop(self):
        """Run in message loop"""

        try:
            MessageLoop(self.bot, self._handler).run_as_thread()
        except Exception as e:
            print(str(e))
            raise
