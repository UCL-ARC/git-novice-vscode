from pathlib import Path

from playwright.sync_api import Page

from ..ui import (
    commit_and_screenshot,
    edit_file,
    open_diff_and_screenshot,
    screenshot_with_dot,
    stage_file_and_screenshot,
    write_file,
)


def tracking_changes(page: Page, desktop: Path, output: Path) -> None:
    # Deselect desserts (from ep3) so the new file goes in the repo root.
    page.keyboard.press("ControlOrMeta+Shift+E")
    page.keyboard.press("Escape")
    write_file(
        page,
        "guacamole.md",
        "# Guacamole\n## Ingredients\n## Instructions\n",
        output / "04-changes-create-file.png",
    )

    page.keyboard.press("Control+Shift+G")
    page.get_by_role("treeitem", name="guacamole.md, Untracked").wait_for()
    page.screenshot(path=output / "04-changes-status-untracked.png")

    stage_file_and_screenshot(page, "guacamole.md", output / "04-changes-add.png")
    commit_and_screenshot(
        page,
        "Create initial structure for a Guacamole recipe",
        output / "04-changes-commit.png",
    )

    page.get_by_role("treeitem", name="Create initial structure for a Guacamole recipe").hover()
    page.get_by_role("tooltip").wait_for()
    page.screenshot(path=output / "04-changes-log.png")

    edit_file(
        page,
        "guacamole.md",
        "# Guacamole\n## Ingredients\n* avocado\n* lemon\n* salt\n## Instructions\n",
        output / "04-changes-edit-ingredients.png",
    )

    page.keyboard.press("Control+Shift+G")
    page.get_by_role("treeitem", name="guacamole.md, Modified").wait_for()
    page.screenshot(path=output / "04-changes-status-modified.png")

    open_diff_and_screenshot(page, "guacamole.md", output / "04-changes-diff.png")

    # Commit before staging: VSCode asks to stage everything, where git would refuse.
    page.get_by_role("textbox", name="Message").press_sequentially(
        "Add ingredients for basic guacamole"
    )
    commit = page.get_by_role("button", name="Commit Changes on")
    screenshot_with_dot(page, commit, output / "04-changes-commit-unstaged.png")
    commit.click()
    cancel = page.get_by_role("dialog").get_by_role("button", name="Cancel")
    screenshot_with_dot(page, cancel, output / "04-changes-commit-unstaged-dialog.png")
    cancel.click()

    stage_file_and_screenshot(page, "guacamole.md", output / "04-changes-add-ingredients.png")
    commit_and_screenshot(
        page, "Add ingredients for basic guacamole", output / "04-changes-commit-ingredients.png"
    )
