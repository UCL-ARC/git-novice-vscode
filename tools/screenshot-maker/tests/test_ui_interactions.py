"""
Test UI interactions

Mostly testing code in screenshot-maker/ui.py. These tests using the vscode_page fixture will be
slow, because we start and then teardown a server instance for each.

Tip: you will want to call `ui.close_annoying_modals` first thing in any test you add here. We
don't add this to the fixture, so we get a more helpful error if the test fails at that point
(which is likely if VSCode changes the modals in later versions).
"""

import pytest
from playwright.sync_api import expect, Page

from screenshot_maker.ui import close_annoying_modals, open_terminal_and_type


def test_00_close_annoying_modals(vscode_page) -> None:
    # Should be able to close the modals and then interact with the page.
    # Any errors here should be fixed before you even look at the rest of the tests in this file.
    close_annoying_modals(vscode_page)
    vscode_page.get_by_role("menuitem", name="Application Menu").click()
    vscode_page.get_by_role("menuitem", name="File", exact=True).click()


@pytest.mark.parametrize(
    "bad_input",
    [
        ["ls -l"],  # one command without newline
        ["ls -l\n", "pwd"],  # one command with newline, one without
        ["ls -l", "pwd\n"],  # one command without newline, one with
        ["ls -l", "pwd"],  # two commands without newlines
    ],
)
def test_terminal_interaction_bad_input(bad_input) -> None:
    with pytest.raises(expected_exception=ValueError):
        open_terminal_and_type(None, commands=bad_input)


def test_terminal_interaction_good_input(vscode_page) -> None:
    # Should be able to Ctrl/Cmd + ` to open a terminal and type something.
    close_annoying_modals(vscode_page)
    open_terminal_and_type(vscode_page, commands=["echo 'Hello, World!'\n"])

    terminal_output = vscode_page.locator(".xterm-rows")
    expect(terminal_output).to_contain_text("Hello, World!")
