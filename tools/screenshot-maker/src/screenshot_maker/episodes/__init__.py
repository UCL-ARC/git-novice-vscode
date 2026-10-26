from collections.abc import Callable
from pathlib import Path

from playwright.sync_api import Page

from .ep0_example import example
from .ep2_setting_up_git import setting_up_git
from .ep3_creating_a_repository import creating_a_repository

Episode = Callable[[Page, Path, Path], None]


EPISODES: list[Episode] = [
    example,
    setting_up_git,
    creating_a_repository,
    # Add more episodes here as we create them.
    # ...
]
