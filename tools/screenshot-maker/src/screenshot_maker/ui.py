"""
Common VSCode UI interaction functions.

If a helper gives an action a clear name and hides repeated Playwright mechanics, it belongs here.
If it only wraps one obvious locator call and is used once, leave it in the episode.
"""

import re
from pathlib import Path

from playwright.sync_api import Page, expect


def close_annoying_modals(page: Page) -> None:
    """Get rid of the annoying modals and popups that block interaction with the page."""
    # None of this is important but it does introduce a brittleness.
    page.get_by_role("button", name="Restricted Mode: Some").click()
    page.get_by_role("button", name="Trust", exact=True).click()
    page.get_by_role("button", name="Close Modal Editor (Escape)").click()


def commit_changes(page: Page, message: str) -> None:
    open_source_control(page)
    page.get_by_role("treeitem", name="Changes", exact=True).hover()
    page.get_by_role("button", name="Stage All Changes").click()
    page.get_by_role("treeitem", name="Staged Changes").wait_for()
    message_box = page.get_by_role("textbox", name="Message")
    message_box.press_sequentially(message)
    message_box.press("ControlOrMeta+Enter")


def init_workspace(page: Page, desktop: Path, name: str) -> None:
    page.get_by_role("menuitem", name="Application Menu").click()
    page.get_by_role("menuitem", name="File", exact=True).click()
    page.get_by_role("menuitem", name="Open Folder...").click(delay=100)
    folder_path = page.get_by_role("textbox", name="Folder path")
    expect(folder_path).to_have_value(f"{desktop.parent}/")
    folder_path.fill(f"{desktop}/{name}")
    expect(page.get_by_role("option", name="Desktop")).to_be_hidden()
    page.get_by_role("button", name="OK").click()  # "create new folder"
    page.get_by_text(f"The folder {name} does not").wait_for()
    page.get_by_role("button", name="OK").click()  # "are you sure?"
    page.wait_for_url(f"**/{name}")
    close_annoying_modals(page)


def make_subfolder(page: Page, name: str) -> None:
    open_file_explorer(page)
    page.get_by_role("button", name="New Folder...", exact=True).click()
    folder_name = page.get_by_role("textbox", name="Type file name")
    folder_name.fill(name)
    folder_name.press("Enter")


def _open_sidebar_view(page: Page, name: str) -> None:
    # Shortcuts are swallowed when e.g. an image preview has focus, so click the tab instead.
    tab = page.get_by_role("tab", name=re.compile(rf"^{name}"))
    if tab.get_attribute("aria-selected") != "true":
        tab.click()
    expect(page.get_by_role("heading", name=name, exact=True)).to_be_visible(timeout=10_000)


def open_source_control(page: Page) -> None:
    """Clicks the 'Source Control' tab in the sidebar and waits for it to be visible."""
    _open_sidebar_view(page, "Source Control")


def open_file_explorer(page: Page) -> None:
    """Clicks the 'File Explorer' tab in the sidebar and waits for it to be visible."""
    _open_sidebar_view(page, "Explorer")


def open_terminal(page: Page) -> None:
    """Opens the terminal and waits for the bash prompt to be ready."""
    page.keyboard.press("Control+Shift+`")
    expect_terminal_to_contain(page, "$")


def init_repo(page: Page) -> None:
    open_source_control(page)
    page.get_by_role("button", name="Initialize Repository").click()
    page.get_by_role("textbox", name="Message").wait_for()


def expect_terminal_to_contain(page: Page, expected: str) -> None:
    """Use this to check (or wait for) terminal output from a call to `type_into_terminal`."""
    terminal_output = page.locator(".xterm-rows")
    expect(terminal_output).to_contain_text(expected)


def type_into_terminal(page: Page, command: str) -> None:
    page.get_by_role("textbox", name="Terminal 1").press_sequentially(f"{command}\n")


def type_into_terminal_and_screenshot(
    page: Page, command: str, screenshot_output_path: Path, expected: str
) -> None:
    type_into_terminal(page, command)
    expect_terminal_to_contain(page, expected)
    page.screenshot(path=screenshot_output_path)


def write_file(page: Page, name: str, content: str = "") -> None:
    open_file_explorer(page)
    page.get_by_role("button", name="New File...", exact=True).click()
    file_name = page.get_by_role("textbox", name="Type file name")
    file_name.fill(name)
    file_name.press("Enter", delay=100)
    if content:
        editor = page.get_by_role("textbox", name=Path(name).name)
        editor.press_sequentially(content)
        editor.press("ControlOrMeta+s", delay=100)
