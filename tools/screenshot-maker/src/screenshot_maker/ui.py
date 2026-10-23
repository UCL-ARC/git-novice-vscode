"""
Common VSCode UI interaction functions.

If a helper gives an action a clear name and hides repeated Playwright mechanics, it belongs here.
If it only wraps one obvious locator call and is used once, leave it in the episode.
"""

from playwright.sync_api import Page


def commit_changes(page: Page, message: str) -> None:
    page.keyboard.press("Control+Shift+G")
    page.get_by_role("treeitem", name="Changes", exact=True).hover()
    page.get_by_role("button", name="Stage All Changes").click()
    page.get_by_role("treeitem", name="Staged Changes").wait_for()
    message_box = page.get_by_role("textbox", name="Message")
    message_box.press_sequentially(message)
    message_box.press("ControlOrMeta+Enter")
