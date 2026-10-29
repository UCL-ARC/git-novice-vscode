from pathlib import Path

from playwright.sync_api import Page

from ..ui import (
    expect_terminal_to_contain,
    init_workspace_and_screenshot,
    open_terminal,
    type_into_terminal,
    type_into_terminal_and_screenshot,
)


def setting_up_git(page: Page, desktop: Path, output: Path) -> None:
    # Use folder in this lesson but create in next.
    init_workspace_and_screenshot(page, desktop, "recipes", output / "03-create-workspace.png")
    page.keyboard.press("ControlOrMeta+B")  # Hide pre-created folder
    open_terminal(page)

    type_into_terminal(page, 'git config --global user.name "Alfredo Linguini"')
    type_into_terminal_and_screenshot(
        page,
        'git config --global user.email "a.linguini@ratatouille.fr"',
        output / "02-setup-name-and-email.png",
        expected='ratatouille.fr"bash-',
    )
    type_into_terminal_and_screenshot(
        page,
        "git config --global core.autocrlf input",
        output / "02-setup-line-endings.png",
        expected="inputbash-",
    )
    type_into_terminal_and_screenshot(
        page,
        'git config --global core.editor "vim"',
        output / "02-setup-editor.png",
        expected='"vim"bash-',
    )
    type_into_terminal_and_screenshot(
        page,
        "git config --global init.defaultBranch main",
        output / "02-setup-default-branch.png",
        expected="mainbash-",
    )
    type_into_terminal_and_screenshot(
        page,
        "git config --global --edit",
        output / "02-setup-edit-config.png",
        expected='.gitconfig"',
    )
    type_into_terminal(page, ":wq")
    expect_terminal_to_contain(page, "--editbash-")
    type_into_terminal(page, "git config --list --global")
    type_into_terminal_and_screenshot(
        page, "G", output / "02-setup-list-config.png", expected="init.defaultbranch=main"
    )
    type_into_terminal(page, "q")
