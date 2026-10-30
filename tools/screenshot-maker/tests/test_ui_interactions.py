"""
Test UI interactions

Mostly testing code in screenshot-maker/ui.py. These tests using the vscode_page fixture will be
slow, because we start and then teardown a server instance for each.

Tip: you will want to call `ui.close_annoying_modals` first thing in any test you add here. We
don't add this to the fixture, so we get a more helpful error if the test fails at that point
(which is likely if VSCode changes the modals in later versions).
"""

from pathlib import Path

from playwright.sync_api import expect

from screenshot_maker.compare import _images_differ
from screenshot_maker.ui import (
    close_annoying_modals,
    open_file_explorer,
    open_source_control,
    make_subfolder_and_screenshot,
    open_terminal,
    screenshot_with_dot,
    type_into_terminal,
    write_file,
)


def test_00_close_annoying_modals(vscode_page) -> None:
    # Should be able to close the modals and then interact with the page.
    # Any errors here should be fixed before you even look at the rest of the tests in this file.
    close_annoying_modals(vscode_page)
    vscode_page.get_by_role("menuitem", name="Application Menu").click()
    vscode_page.get_by_role("menuitem", name="File", exact=True).click()


def test_terminal_interaction(vscode_page) -> None:
    # Should be able to Ctrl/Cmd + ` to open a terminal and type something.
    close_annoying_modals(vscode_page)
    open_terminal(vscode_page)

    # The typed command contains the pieces separately, so the joined text only appears if it ran.
    type_into_terminal(vscode_page, command="echo 'Hello, ''World''!'")

    terminal_output = vscode_page.locator(".xterm-rows")
    expect(terminal_output).to_contain_text("'Hello, ''World''!'")  # the command should be visible
    expect(terminal_output).to_contain_text("Hello, World!")  # the output of the command


def test_make_subfolder(vscode_page_and_path, tmp_path_factory) -> None:
    # Should be able to make a subfolder in the workspace, with a screenshot of each step.
    vscode_page, tmp_path = vscode_page_and_path
    screenshots = tmp_path_factory.mktemp("screenshots")
    close_annoying_modals(vscode_page)
    make_subfolder_and_screenshot(vscode_page, "test_folder", screenshots / "subfolder.png")
    assert (tmp_path / "test_folder").is_dir()
    assert sorted(path.name for path in screenshots.iterdir()) == [
        "subfolder-after.png",
        "subfolder-name.png",
        "subfolder.png",
    ]


def test_write_file(vscode_page_and_path) -> None:
    # Should be able to write a file in the workspace.
    vscode_page, tmp_path = vscode_page_and_path
    close_annoying_modals(vscode_page)
    write_file(vscode_page, "test_file.txt", "Hello, World!")
    assert (tmp_path / "test_file.txt").exists()
    assert (tmp_path / "test_file.txt").is_file()
    assert (tmp_path / "test_file.txt").read_text() == "Hello, World!"


def test_write_file_into_subfolder(vscode_page_and_path) -> None:
    # Should be able to write a file in the workspace with a subfolder in the file name.
    vscode_page, tmp_path = vscode_page_and_path
    close_annoying_modals(vscode_page)
    write_file(vscode_page, "test_folder/test_file.txt", "Hello, World!")
    assert (tmp_path / "test_folder").exists()
    assert (tmp_path / "test_folder").is_dir()
    assert (tmp_path / "test_folder" / "test_file.txt").exists()
    assert (tmp_path / "test_folder" / "test_file.txt").is_file()
    assert (tmp_path / "test_folder" / "test_file.txt").read_text() == "Hello, World!"


def test_open_source_control(vscode_page) -> None:
    # Should be able to open the source control pane.
    close_annoying_modals(vscode_page)
    open_source_control(vscode_page)
    expect(vscode_page.get_by_role("heading", name="Source Control")).to_be_visible()


def test_open_file_explorer(vscode_page) -> None:
    # Should be able to open the file explorer pane.
    close_annoying_modals(vscode_page)
    open_file_explorer(vscode_page)
    expect(vscode_page.get_by_role("heading", name="Explorer", exact=True)).to_be_visible()


PATH_TO_DEMO_PAGE = Path(__file__).parent.resolve() / "data" / "demo-page.html"


def _assert_images_are_equal(actual: Path, expected: Path) -> None:
    assert not _images_differ(actual, expected), f"Images differ: {actual} vs {expected}"


def test_screenshot_with_dot(page, tmp_path) -> None:
    assert PATH_TO_DEMO_PAGE.is_file()
    page.goto(f"file://{PATH_TO_DEMO_PAGE}")
    demo_button = page.get_by_role("button", name="click me")

    obtained = tmp_path / "demo-button-dot.png"
    screenshot_with_dot(page, demo_button, obtained)
    assert obtained.is_file(), "Screenshot was not created"

    expected = PATH_TO_DEMO_PAGE.parent / "demo-button-dot.png"
    _assert_images_are_equal(obtained, expected)
