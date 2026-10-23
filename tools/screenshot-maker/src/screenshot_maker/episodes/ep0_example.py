"""David's example."""

from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import close_annoying_modals, commit_changes, open_terminal_and_type


def example(page: Page, desktop: Path) -> None:
    # Open and name folder
    page.get_by_role("menuitem", name="Application Menu").click()
    page.get_by_role("menuitem", name="File", exact=True).click()
    page.get_by_role("menuitem", name="Open Folder...").click(delay=100)
    folder_path = page.get_by_role("textbox", name="Folder path")
    expect(folder_path).to_have_value(f"{desktop.parent}/")
    folder_path.fill(f"{desktop}/test_repo")
    expect(page.get_by_role("option", name="Desktop")).to_be_hidden()
    page.get_by_role("button", name="OK").click()  # "create new folder"
    page.get_by_text("The folder test_repo does not").wait_for()
    page.get_by_role("button", name="OK").click()  # "are you sure?"
    page.wait_for_url("**/test_repo")

    # Trust folder and Init repo
    page.get_by_role("button", name="Restricted Mode: Some").click()
    page.get_by_role("button", name="Trust", exact=True).click()
    page.get_by_role("button", name="Close Modal Editor (Escape)").click()
    page.keyboard.press("Control+Shift+G")
    page.get_by_role("button", name="Initialize Repository").click()
    page.get_by_role("textbox", name="Message").wait_for()

    # Set git identity
    git_config_commands = [
        'git config user.name "Alfredo Linguini"\n',
        'git config user.email "a.linguini@ratatouille.fr"\n',
    ]
    open_terminal_and_type(page, git_config_commands)

    # Make new file and fill with Gucamole
    page.keyboard.press("ControlOrMeta+Shift+E")
    page.get_by_role("button", name="New File...", exact=True).click()
    file_name = page.get_by_role("textbox", name="Type file name")
    file_name.fill("guacamole.md")
    file_name.press("Enter")
    editor = page.get_by_role("textbox", name="guacamole.md")
    editor.press_sequentially("# Guacamole\n## Ingredients\n\n## Instructions\n")
    editor.press("ControlOrMeta+s")

    commit_changes(page, "Defines template")
    expect(page.get_by_role("treeitem", name="Staged Changes")).to_be_hidden()

    # Look through files and take a screenshot
    terminal_output = page.locator(".xterm-rows")
    open_terminal_and_type(page, ["clear\n", "ls -a\n"])
    expect(terminal_output).to_contain_text(".git")
    expect(terminal_output).to_contain_text(".git")
    page.screenshot(path="fin.png")
