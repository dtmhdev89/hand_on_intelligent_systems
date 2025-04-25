import sys
import os

app_up_levels = [".."] * 1
PACKAGE_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        *app_up_levels
    )
)

project_up_levels = [".."] * 2
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        *project_up_levels
    )
)

if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# import_packages = [
#     "simple_ai_text_image_prompt_app"
# ]

# for idx, package_name in enumerate(import_packages):
#     package_path = os.path.join(PROJECT_ROOT, package_name)
#     if package_path not in sys.path:
#         sys.path.insert(idx + 2, package_path)
