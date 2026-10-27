"""
Common VSCode UI interaction functions.

If a helper gives an action a clear name and hides repeated Playwright mechanics, it belongs here.
If it only wraps one obvious locator call and is used once, leave it in the episode.
"""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import FloatRect, Locator, Page, Position, expect


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
    page.keyboard.press("ControlOrMeta+Shift+E")
    page.get_by_role("button", name="New Folder...", exact=True).click()
    folder_name = page.get_by_role("textbox", name="Type file name")
    folder_name.fill(name)
    folder_name.press("Enter")


def init_repo(page: Page) -> None:
    page.keyboard.press("Control+Shift+G")
    page.get_by_role("button", name="Initialize Repository").click()
    page.get_by_role("textbox", name="Message").wait_for()


def expect_terminal_to_contain(page: Page, expected: str) -> None:
    """Use this to check (or wait for) terminal output from a call to `type_into_terminal`."""
    terminal_output = page.locator(".xterm-rows")
    expect(terminal_output).to_contain_text(expected)


def open_terminal(page: Page) -> None:
    page.keyboard.press("Control+Shift+`")
    expect_terminal_to_contain(page, "$")


def type_into_terminal(page: Page, command: str) -> None:
    page.get_by_role("textbox", name="Terminal 1").press_sequentially(f"{command}\n")


def type_into_terminal_and_screenshot(
    page: Page, command: str, screenshot_output_path: Path, expected: str
) -> None:
    type_into_terminal(page, command)
    expect_terminal_to_contain(page, expected)
    page.screenshot(path=screenshot_output_path)


def write_file(page: Page, name: str, content: str) -> None:
    page.keyboard.press("ControlOrMeta+Shift+E")
    page.get_by_role("button", name="New File...", exact=True).click()
    file_name = page.get_by_role("textbox", name="Type file name")
    file_name.fill(name)
    file_name.press("Enter")
    editor = page.get_by_role("textbox", name=name)
    editor.press_sequentially(content)
    editor.press("ControlOrMeta+s", delay=500)


def _centre(box: FloatRect) -> Position:
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    return Position(x=x, y=y)


def screenshot_with_dot(
    page: Page, locator: Locator, output: Path, radius: int = 7, width: int = 3
):
    locator.hover()

    box = locator.bounding_box()
    if box is None:
        raise ValueError(f"Could not get a bounding box from {locator}")
    point = _centre(box)

    scale = page.evaluate("window.devicePixelRatio")
    x, y = point["x"] * scale, point["y"] * scale
    r, w = radius * scale, round(width * scale)

    img = Image.open(BytesIO(page.screenshot())).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.ellipse((x - r, y - r, x + r, y + r), outline="red", width=w)
    img.save(output)
