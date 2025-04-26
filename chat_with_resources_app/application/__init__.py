import os
import sys


def add_project_root_to_system_path():
    """Add project root path to system path"""

    project_up_levels = [".."] * 2

    PROJECT_ROOT = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            *project_up_levels
        )
    )

    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)


if __name__ == "__main__":
    add_project_root_to_system_path()
