from collections.abc import Callable
from pathlib import Path

from playwright.sync_api import Page

from .ep02_setup import setting_up_git
from .ep03_create import creating_a_repository
from .ep06_ignore import ignoring_things

Episode = Callable[[Page, Path, Path], None]


EPISODES: list[Episode] = [
    setting_up_git,
    creating_a_repository,
    ignoring_things,
    # Add more episodes here as we create them.
    # ...
]
