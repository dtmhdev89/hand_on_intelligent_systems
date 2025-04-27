import os
import sys

up_levels = [".."] * 2

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        *up_levels
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from jarvis_agi_virtual_assistant.config.settings import load_dotenv

load_dotenv()
