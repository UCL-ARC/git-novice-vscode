from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import (
    commit_and_screenshot,
    edit_file,
    open_diff_and_screenshot,
    screenshot_with_box,
    screenshot_with_dot,
    stage_file_and_screenshot,
    type_into_terminal,
    write_file,
)


def tracking_changes(page: Page, desktop: Path, output: Path) -> None:
    type_into_terminal(page, "clear")
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
    untracked = page.get_by_role("treeitem", name="guacamole.md, Untracked")
    untracked.wait_for()
    screenshot_with_box(page, untracked, output / "04-changes-status-untracked.png")

    stage_file_and_screenshot(page, "guacamole.md", output / "04-changes-add.png")
    commit_and_screenshot(
        page,
        "Create initial structure for a Guacamole recipe",
        output / "04-changes-commit.png",
    )
    page.get_by_role("treeitem", name="Create initial structure for a Guacamole recipe").wait_for()
    history = page.get_by_role("tree", name="Source Control History")
    screenshot_with_box(page, history, output / "04-changes-commit-log.png")

    edit_file(
        page,
        "guacamole.md",
        "# Guacamole\n## Ingredients\n* avocado\n* lemon\n* salt\n## Instructions\n",
        output / "04-changes-edit-ingredients.png",
    )

    page.keyboard.press("Control+Shift+G")
    modified = page.get_by_role("treeitem", name="guacamole.md, Modified")
    modified.wait_for()
    screenshot_with_box(page, modified, output / "04-changes-status-modified.png")

    open_diff_and_screenshot(page, "guacamole.md", output / "04-changes-diff.png")
    working_tree = page.get_by_role("tab", name="guacamole.md (Working Tree)")
    working_tree.get_by_role("button", name="Close").click()
    expect(working_tree).to_be_hidden()

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

    edit_file(
        page,
        "guacamole.md",
        "# Guacamole\n## Ingredients\n* avocado\n* lime\n* salt\n## Instructions\n",
        output / "04-changes-lime.png",
    )
    open_diff_and_screenshot(page, "guacamole.md", output / "04-changes-lime-diff.png")
    stage_file_and_screenshot(page, "guacamole.md", output / "04-changes-lime-add.png")
    open_diff_and_screenshot(
        page, "guacamole.md", output / "04-changes-lime-diff-staged.png", staged=True
    )
    commit_and_screenshot(
        page, "Modify guacamole to the traditional recipe", output / "04-changes-lime-commit.png"
    )

    page.get_by_role("treeitem", name="Modify guacamole to the traditional recipe").wait_for()
    history = page.get_by_role("tree", name="Source Control History")
    screenshot_with_box(page, history, output / "04-changes-log.png")
