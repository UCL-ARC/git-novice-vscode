"""
Common VSCode UI interaction functions.

If a helper gives an action a clear name and hides repeated Playwright mechanics, it belongs here.
If it only wraps one obvious locator call and is used once, leave it in the episode.
"""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import FloatRect, Locator, Page, Position, expect


def _centre(box: FloatRect) -> Position:
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    return Position(x=x, y=y)


def _screenshot(page: Page, path: Path) -> None:
    # The mouse stays wherever the last click was, so a tooltip or a highlighted resize handle can
    # end up in the shot depending on timing. The top-left corner of the page is empty.
    page.mouse.move(0, 0)
    page.screenshot(animations="disabled", path=path)


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

    img = Image.open(BytesIO(page.screenshot(animations="disabled"))).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.ellipse((x - r, y - r, x + r, y + r), outline="red", width=w)
    img.save(output)


def screenshot_with_box(page: Page, locator: Locator, output: Path, width: int = 3):
    page.mouse.move(0, 0)
    box = locator.bounding_box()
    if box is None:
        raise ValueError(f"Could not get a bounding box from {locator}")

    scale = page.evaluate("window.devicePixelRatio")
    x, y = box["x"] * scale, box["y"] * scale
    x1, y1 = x + box["width"] * scale, y + box["height"] * scale

    img = Image.open(BytesIO(page.screenshot(animations="disabled"))).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.rectangle((x, y, x1, y1), outline="red", width=round(width * scale))
    img.save(output)


def close_annoying_modals(page: Page, screenshot_output_path: Path | None = None) -> None:
    """Get rid of the annoying modals and popups that block interaction with the page."""
    # None of this is important but it does introduce a brittleness.
    buttons = {
        "restricted-mode": page.get_by_role("button", name="Restricted Mode: Some"),
        "trust": page.get_by_role("button", name="Trust", exact=True),
        "close-modal": page.get_by_role("button", name="Close Modal Editor (Escape)"),
    }
    for suffix, button in buttons.items():
        if screenshot_output_path:
            screenshot_name = screenshot_output_path.stem
            screenshot_with_dot(
                page, button, screenshot_output_path.with_stem(f"{screenshot_name}-{suffix}")
            )
        button.click()


def close_secondary_sidebar(page: Page) -> None:
    page.get_by_text("Restricted Mode is intended for safe code browsing").wait_for()
    hide_sidebar = page.get_by_role("button", name="Hide Secondary Side Bar")
    if hide_sidebar.is_visible():
        hide_sidebar.click()


def commit_changes(page: Page, message: str) -> None:
    page.keyboard.press("Control+Shift+G")
    page.get_by_role("treeitem", name="Changes", exact=True).hover()
    page.get_by_role("button", name="Stage All Changes").click()
    page.get_by_role("treeitem", name="Staged Changes").wait_for()
    message_box = page.get_by_role("textbox", name="Message")
    message_box.press_sequentially(message)
    message_box.press("ControlOrMeta+Enter")


def init_workspace_and_screenshot(
    page: Page,
    desktop: Path,
    name: str,
    screenshot_output_path: Path,
) -> None:
    close_secondary_sidebar(page)
    page.get_by_role("menuitem", name="Application Menu").click()
    page.get_by_role("menuitem", name="File", exact=True).click()
    open_folder = page.get_by_role("menuitem", name="Open Folder...")
    screenshot_with_dot(page, open_folder, screenshot_output_path)
    open_folder.click(delay=100)

    folder_path = page.get_by_role("textbox", name="Folder path")
    expect(folder_path).to_have_value(f"{desktop.parent}/")
    real_path = f"{desktop}/{name}"
    fake_path = f"/Users/Alfredo/Desktop/{name}"
    show_path = "(element, path) => element.value = path"
    folder_path.fill(real_path)
    expect(page.get_by_role("option", name="Desktop")).to_be_hidden()
    ok_button = page.get_by_role("button", name="OK")
    screenshot_name = screenshot_output_path.stem

    folder_path.evaluate(show_path, fake_path)
    screenshot_with_dot(
        page, ok_button, screenshot_output_path.with_stem(f"{screenshot_name}-new-folder")
    )
    folder_path.evaluate(show_path, real_path)
    ok_button.click()  # "create new folder"
    page.get_by_text(f"The folder {name} does not").wait_for()

    confirm_path = page.get_by_role("textbox", name=f"The folder {name} does not")
    confirm_path.evaluate(show_path, fake_path)
    screenshot_with_dot(
        page, ok_button, screenshot_output_path.with_stem(f"{screenshot_name}-confirm")
    )
    confirm_path.evaluate(show_path, real_path)
    ok_button.click()  # "are you sure?"
    page.wait_for_url(f"**/{name}")
    close_secondary_sidebar(page)
    close_annoying_modals(page, screenshot_output_path)


def make_subfolder_and_screenshot(page: Page, name: str, screenshot_output_path: Path) -> None:
    page.keyboard.press("ControlOrMeta+Shift+E")
    page.get_by_role("button", name="Explorer Section:").hover()
    new_folder = page.get_by_role("button", name="New Folder...", exact=True)
    screenshot_name = screenshot_output_path.stem
    screenshot_with_dot(page, new_folder, screenshot_output_path)
    new_folder.click()
    folder_name = page.get_by_role("textbox", name="Type file name")
    folder_name.fill(name)
    _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-name"))
    folder_name.press("Enter")
    page.get_by_role("treeitem", name=name).wait_for()
    _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-after"))


def init_repo_and_screenshot(page: Page, screenshot_output_path: Path) -> None:
    page.keyboard.press("Control+Shift+G")
    initialise = page.get_by_role("button", name="Initialize Repository")
    screenshot_with_dot(page, initialise, screenshot_output_path)
    initialise.click()
    page.get_by_role("textbox", name="Message").wait_for()
    page.get_by_text("does not have any source control history items").wait_for()
    screenshot_name = screenshot_output_path.stem
    _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-after-click"))


def stage_file_and_screenshot(page: Page, name: str, screenshot_output_path: Path) -> None:
    page.keyboard.press("Control+Shift+G")
    file = page.get_by_role("treeitem", name=f"{name}, ")
    file.hover()
    stage = file.get_by_role("button", name="Stage Changes")
    screenshot_with_dot(page, stage, screenshot_output_path)
    stage.click()
    page.get_by_role("treeitem", name="Staged Changes").wait_for()
    screenshot_name = screenshot_output_path.stem
    _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-after"))


def open_diff_and_screenshot(
    page: Page, name: str, screenshot_output_path: Path, staged: bool = False
) -> None:
    page.keyboard.press("Control+Shift+G")
    file = page.get_by_role("treeitem", name=f"{name}, ")
    screenshot_with_dot(page, file, screenshot_output_path)
    file.click()
    side = "Index" if staged else "Working Tree"
    page.get_by_role("tab", name=f"{name} ({side})").wait_for()
    page.locator(".monaco-diff-editor").locator(".line-insert, .line-delete").first.wait_for()
    screenshot_name = screenshot_output_path.stem
    _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-after"))


def commit_and_screenshot(page: Page, message: str, screenshot_output_path: Path) -> None:
    page.keyboard.press("Control+Shift+G")
    message_box = page.get_by_role("textbox", name="Message")
    message_box.press("ControlOrMeta+a")
    message_box.press_sequentially(message)
    commit = page.get_by_role("button", name="Commit Changes on")
    screenshot_with_dot(page, commit, screenshot_output_path)
    commit.click()
    expect(page.get_by_role("treeitem", name="Staged Changes")).to_be_hidden()
    # The change bars and any open diff stay drawn for a moment after the commit: wait for them.
    expect(page.locator(".dirty-diff-glyph, .line-insert, .line-delete")).to_have_count(0)
    page.get_by_role("treeitem", name=message).wait_for()
    expect(page.locator(".progress-badge")).to_have_count(0)
    screenshot_name = screenshot_output_path.stem
    _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-after"))


def expect_terminal_to_contain(page: Page, expected: str) -> None:
    """Use this to check (or wait for) terminal output from a call to `type_into_terminal`."""
    terminal_output = page.locator(".xterm-rows")
    expect(terminal_output).to_contain_text(expected)
    expect(page.locator(".xterm-scrollbar.xterm-visible")).to_have_count(0)


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
    _screenshot(page, screenshot_output_path)


def write_file(
    page: Page, name: str, content: str, screenshot_output_path: Path | None = None
) -> None:
    page.keyboard.press("ControlOrMeta+Shift+E")
    page.get_by_role("button", name="Explorer Section:").hover()
    new_file = page.get_by_role("button", name="New File...", exact=True)
    if screenshot_output_path:
        screenshot_name = screenshot_output_path.stem
        screenshot_with_dot(page, new_file, screenshot_output_path)
    new_file.click()
    file_name = page.get_by_role("textbox", name="Type file name")
    file_name.fill(name)
    if screenshot_output_path:
        _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-name"))
    file_name.press("Enter")
    editor = page.get_by_role("textbox", name=name)
    editor.press_sequentially(content)
    editor.press("ControlOrMeta+s", delay=500)
    if screenshot_output_path:
        page.locator(".tab.active .monaco-decoration-text-badge").wait_for()
        _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-after"))


def edit_file(
    page: Page, name: str, content: str, screenshot_output_path: Path | None = None
) -> None:
    page.keyboard.press("ControlOrMeta+Shift+E")
    file = page.get_by_role("treeitem", name=name)
    if screenshot_output_path:
        screenshot_name = screenshot_output_path.stem
        screenshot_with_dot(page, file, screenshot_output_path)
    file.click()
    editor = page.get_by_role("textbox", name=name)
    editor.press("ControlOrMeta+a")
    editor.press_sequentially(content)
    editor.press("ControlOrMeta+s", delay=500)
    if screenshot_output_path:
        page.locator(".tab.active .monaco-decoration-text-badge").wait_for()
        _screenshot(page, screenshot_output_path.with_stem(f"{screenshot_name}-after"))
