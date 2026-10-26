from collections.abc import Callable
from pathlib import Path

from playwright.sync_api import Page

from .ep0_example import example
from .ep02_setup import setting_up_git  # noqa: F401
from .ep03_create import creating_a_repository  # noqa: F401
from .ep06_ignore import ignoring_things

Episode = Callable[[Page, Path, Path], None]


EPISODES: list[Episode] = [
    example,
    ignoring_things,
    # Add more episodes here as we create them.
    # episodes.setting_up_git,
    # episodes.creating_a_repository,
    # ...
]
