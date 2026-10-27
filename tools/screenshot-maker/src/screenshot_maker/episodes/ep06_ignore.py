import re
from pathlib import Path

from playwright.sync_api import Page

from ..ui import (
    open_source_control,
    # make_subfolder,
    write_file,
)


def ignoring_things(page: Page, desktop: Path, output: Path):
    # Create some files and a subfolder in the workspace.
    write_file(page, "a.png")
    write_file(page, "b.png")
    write_file(page, "pictures/cake1.jpg")
    write_file(page, "cake2.jpg")  # will be in the subdirectory

    # Take a screenshot of the "pictures" folder in the file explorer.
    page.get_by_label(f"{desktop}/pictures", exact=True).locator("div").filter(
        has_text=re.compile(r"^pictures$")
    )
    page.screenshot(path=output / "06-ignore-empty-images.png")

    # Open the Source Control pane and take a screenshot of the untracked files.
    open_source_control(page)
    page.screenshot(path=output / "06-ignore-untracked-image-files.png")

    # Add a .gitignore
    write_file(page, ".gitignore", content="*.png\npictures/\n")
    open_source_control(page)
    page.screenshot(path=output / "06-ignore-gitignored.png")
