"""
Common VSCode UI interaction functions.

If a helper gives an action a clear name and hides repeated Playwright mechanics, it belongs here.
If it only wraps one obvious locator call and is used once, leave it in the episode.
"""

from loguru import logger
from playwright.sync_api import Page, expect


def close_annoying_modals(page: Page) -> None:
    """Get rid of the annoying modals and popups that block interaction with the page."""
    # None of this is important but it does introduce a brittleness.
    page.get_by_role("button", name="Restricted Mode: Some").click()
    page.get_by_role("button", name="Trust", exact=True).click()
    page.get_by_role("button", name="Close Modal Editor (Escape)").click()


def commit_changes(page: Page, message: str) -> None:
    page.keyboard.press("Control+Shift+G")
    page.get_by_role("treeitem", name="Changes", exact=True).hover()
    page.get_by_role("button", name="Stage All Changes").click()
    page.get_by_role("treeitem", name="Staged Changes").wait_for()
    message_box = page.get_by_role("textbox", name="Message")
    message_box.press_sequentially(message)
    message_box.press("ControlOrMeta+Enter")


def open_terminal_and_type(page: Page, commands: list[str]) -> None:
    """
    Open the terminal pane and type commands.

    The commands should end with \n to simulate pressing Enter.

    Args:
        page: The Playwright page object.
        commands: A list of commands to type into the terminal.
    """
    if not all(command.endswith("\n") for command in commands):
        raise ValueError("All commands must end with a newline character '\\n'.")

    page.keyboard.press("Control+Shift+`")
    terminal = page.get_by_role("textbox", name="Terminal 1")
    terminal_output = page.locator(".xterm-rows")
    expect(terminal_output).to_contain_text("$")
    logger.info("Typing into terminal pane...")
    for command in commands:
        terminal.press_sequentially(command)
