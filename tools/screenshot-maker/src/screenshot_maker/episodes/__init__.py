from collections.abc import Callable
from pathlib import Path

from playwright.sync_api import Page

from .ep2_setting_up_git import setting_up_git
from .ep3_creating_a_repository import creating_a_repository
from .ep4_tracking_changes import tracking_changes
from .ep6_ignoring_things import ignoring_things

Episode = Callable[[Page, Path, Path], None]

EPISODES: list[Episode] = [
    setting_up_git,
    creating_a_repository,
    ignoring_things,
    tracking_changes,
    # Add more episodes here as we create them.
    # ...
]
