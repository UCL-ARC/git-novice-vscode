from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import (
    init_repo_and_screenshot,
    make_subfolder_and_screenshot,
    type_into_terminal,
    type_into_terminal_and_screenshot,
)


def creating_a_repository(page: Page, desktop: Path, output: Path) -> None:
    # Created workspace in ep2 - named after ep3
    type_into_terminal(page, "clear")
    init_repo_and_screenshot(page, output / "03-create-repo.png")

    page.keyboard.press("ControlOrMeta+Shift+E")
    expect(page.get_by_role("button", name="New File...", exact=True)).to_be_visible()
    # Bounding box hover needed
    page.screenshot(path=output / "03-create-file.png")

    type_into_terminal_and_screenshot(page, "ls", output / "03-create-ls", expected="$")
    type_into_terminal_and_screenshot(page, "ls -a", output / "03-create-ls-a", expected=".git")

    page.keyboard.press("ControlOrMeta+Shift+G")
    page.screenshot(path=output / "03-create-status.png")

    type_into_terminal(page, "cd ~/Desktop\ncd recipes\nls -a")
    make_subfolder_and_screenshot(page, "desserts", output / "03-create-dessert")
