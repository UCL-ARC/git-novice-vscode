from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import init_repo


def creating_a_repository(page: Page, desktop: Path, output: Path) -> None:
    init_repo(page)  # needs a screenshot within because init repo is within this func
    page.screenshot(path=output / "03-create-init.png")

    page.keyboard.press("ControlOrMeta+Shift+E")
    expect(page.get_by_role("button", name="New File...", exact=True)).to_be_visible()
    page.screenshot(path=output / "03-create-ls.png")
