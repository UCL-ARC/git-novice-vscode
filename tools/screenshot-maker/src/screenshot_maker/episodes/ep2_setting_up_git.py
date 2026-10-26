from pathlib import Path

from playwright.sync_api import Page

from ..ui import (
    init_workspace,
    open_terminal,
    type_into_terminal,
    type_into_terminal_and_screenshot,
)


def setting_up_git(page: Page, desktop: Path, output: Path) -> None:
    init_workspace(page, desktop, "recipes")
    open_terminal(page)

    type_into_terminal(page, 'git config --global user.name "Alfredo Linguini"')
    type_into_terminal_and_screenshot(
        page,
        'git config --global user.email "a.linguini@ratatouille.fr"',
        output / "02-setup-name-and-email.png",
    )
    type_into_terminal_and_screenshot(
        page, "git config --global core.autocrlf input", output / "02-setup-line-endings.png"
    )
    type_into_terminal_and_screenshot(
        page, 'git config --global core.editor "vim"', output / "02-setup-editor.png"
    )
    type_into_terminal_and_screenshot(
        page,
        "git config --global init.defaultBranch main",
        output / "02-setup-default-branch.png",
    )
    type_into_terminal_and_screenshot(
        page, "git config --global --edit", output / "02-setup-edit-config.png"
    )
    type_into_terminal(page, ":wq")
    type_into_terminal(page, "git config --list --global")
    type_into_terminal_and_screenshot(
        page, "G", output / "02-setup-list-config.png", expected="init.defaultbranch=main"
    )
    type_into_terminal(page, "q")
