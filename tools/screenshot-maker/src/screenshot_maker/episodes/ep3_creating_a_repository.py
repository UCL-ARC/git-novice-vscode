from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import init_repo, screenshot_with_dot


def creating_a_repository(page: Page, desktop: Path, output: Path) -> None:
    init_repo(page)  # needs a screenshot within because init repo is within this func
    page.screenshot(path=output / "03-create-init.png")

    page.keyboard.press("ControlOrMeta+Shift+E")
    file_location = page.get_by_role("button", name="New File...", exact=True)
    expect(file_location).to_be_visible()
    screenshot_with_dot(page, file_location, output / "03-create-file.png", radius=16)

    page.screenshot(path=output / "03-create-ls.png")
