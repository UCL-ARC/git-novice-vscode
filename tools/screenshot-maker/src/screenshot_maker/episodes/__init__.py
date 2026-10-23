from collections.abc import Callable
from pathlib import Path

from playwright.sync_api import Page

from .ep0_example import example
from .ep2_setting_up_git import setting_up_git  # noqa: F401
from .ep3_creating_a_repository import creating_a_repository  # noqa: F401

Episode = Callable[[Page, Path], None]


EPISODES: list[Episode] = [
    example,
    # Add more episodes here as we create them.
    # episodes.setting_up_git,
    # episodes.creating_a_repository,
    # ...
]
