import re
from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import (
    write_file,
    open_source_control,
    # make_subfolder,
)


def ignoring_things(page: Page, desktop: Path, output: Path):
    # Create some files and a subfolder in the workspace.
    write_file(page, "a.png", content=None)
    write_file(page, "b.png", content=None)
    write_file(page, "pictures/cake1.jpg", content=None)
    write_file(page, "cake2.jpg", content=None)

    # Take a screenshot of the "pictures" folder in the file explorer.
    page.get_by_label(f"{desktop}/pictures", exact=True).locator("div").filter(
        has_text=re.compile(r"^pictures$")
    )
    page.screenshot(path=output / "ep06_ignore_01_pictures.png")

    # Open the Source Control pane and take a screenshot of the untracked files.
    open_source_control(page)
    page.screenshot(path=output / "ep06_ignore_02_untracked_image_files.png")

    # Add a .gitignore
    write_file(page, ".gitignore", content="*.png\npictures/\n")
    open_source_control(page)
    page.screenshot(path=output / "ep06_ignore_03_ignored_images.png")
