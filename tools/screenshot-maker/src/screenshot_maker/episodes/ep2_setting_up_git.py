from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import expect_terminal_to_contain, open_terminal, type_into_terminal


def setting_up_git(page: Page, desktop: Path, output: Path) -> None:
    open_terminal(page)

    type_into_terminal(page, 'git config --global user.name "Alfredo Linguini"')
    type_into_terminal(page, 'git config --global user.email "a.linguini@ratatouille.fr"')
    expect_terminal_to_contain(page, "a.linguini@ratatouille.fr")
    page.screenshot(path=output / "02-setup-name-and-email.png")

    type_into_terminal(page, "git config --global core.autocrlf input")
    expect_terminal_to_contain(page, "core.autocrlf input")
    page.screenshot(path=output / "02-setup-line-endings.png")

    type_into_terminal(page, 'git config --global core.editor "code --wait"')
    expect_terminal_to_contain(page, "code --wait")
    page.screenshot(path=output / "02-setup-editor.png")

    type_into_terminal(page, "git config --global init.defaultBranch main")
    expect_terminal_to_contain(page, "init.defaultBranch main")
    page.screenshot(path=output / "02-setup-default-branch.png")

    type_into_terminal(page, "git config --global --edit")
    config_tab = page.get_by_role("tab", name=".gitconfig")
    expect(config_tab).to_be_visible()
    page.screenshot(path=output / "02-setup-edit.png")
    config_tab.get_by_role("button", name="Close").click()
    expect(config_tab).to_be_hidden()

    type_into_terminal(page, "git config --list --global")
    expect_terminal_to_contain(page, "init.defaultbranch=main")
    page.screenshot(path=output / "02-setup-list.png")
