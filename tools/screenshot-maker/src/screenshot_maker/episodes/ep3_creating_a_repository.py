from pathlib import Path

from playwright.sync_api import Page

from ..ui import (
    init_repo_and_screenshot,
    make_subfolder_and_screenshot,
    screenshot_with_box,
    type_into_terminal,
    type_into_terminal_and_screenshot,
)


def creating_a_repository(page: Page, desktop: Path, output: Path) -> None:
    # Created workspace in ep2 - named after ep3
    type_into_terminal(page, r"clear && printf '\033[3J'")
    init_repo_and_screenshot(page, output / "03-create-repo.png")

    page.keyboard.press("ControlOrMeta+Shift+E")

    type_into_terminal_and_screenshot(page, "ls", output / "03-create-ls.png", expected="lsbash-")
    type_into_terminal_and_screenshot(
        page, "ls -a", output / "03-create-ls-a.png", expected=".git"
    )

    page.keyboard.press("Control+Shift+G")
    page.get_by_role("textbox", name="Message").wait_for()
    changes = page.get_by_role("tree", name="Source Control Management")
    screenshot_with_box(page, changes, output / "03-create-status.png")

    make_subfolder_and_screenshot(page, "desserts", output / "03-create-dessert.png")
