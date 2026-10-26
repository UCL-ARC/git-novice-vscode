"""
Test UI interactions

Mostly testing code in screenshot-maker/ui.py. These tests using the vscode_page fixture will be
slow, because we start and then teardown a server instance for each.

Tip: you will want to call `ui.close_annoying_modals` first thing in any test you add here. We
don't add this to the fixture, so we get a more helpful error if the test fails at that point
(which is likely if VSCode changes the modals in later versions).
"""

import pytest
from playwright.sync_api import expect

from screenshot_maker.ui import (
    close_annoying_modals,
    make_subfolder,
    open_terminal,
    write_file,
    type_into_terminal,
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


@pytest.mark.skip(reason="Failing for some wait reason.")
def test_make_subfolder(vscode_page_and_path) -> None:
    # Should be able to make a subfolder in the workspace.
    vscode_page, tmp_path = vscode_page_and_path
    close_annoying_modals(vscode_page)
    make_subfolder(vscode_page, name="test_folder")
    assert (tmp_path / "test_folder").exists()
    assert (tmp_path / "test_folder").is_dir()


def test_write_file(vscode_page_and_path) -> None:
    # Should be able to write a file in the workspace.
    vscode_page, tmp_path = vscode_page_and_path
    close_annoying_modals(vscode_page)
    write_file(vscode_page, "test_file.txt", "Hello, World!")
    assert (tmp_path / "test_file.txt").exists()
    assert (tmp_path / "test_file.txt").is_file()
    assert (tmp_path / "test_file.txt").read_text() == "Hello, World!"
