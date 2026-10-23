"""David's example."""

from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import (
    commit_changes,
    init_repo,
    init_workspace,
    open_terminal,
    type_into_terminal,
    write_file,
)


def example(page: Page, desktop: Path) -> None:
    # Open, name and trust folder, then init repo
    init_workspace(page, desktop, "test_repo")
    init_repo(page)

    # Set git identity
    open_terminal(page)
    type_into_terminal(page, 'git config user.name "Alfredo Linguini"')
    type_into_terminal(page, 'git config user.email "a.linguini@ratatouille.fr"')

    # Make new file and fill with Gucamole
    write_file(page, "guacamole.md", "# Guacamole\n## Ingredients\n\n## Instructions\n")

    commit_changes(page, "Defines template")
    expect(page.get_by_role("treeitem", name="Staged Changes")).to_be_hidden()

    # Look through files and take a screenshot
    type_into_terminal(page, "clear")
    type_into_terminal(page, "ls -a")
    expect(page.locator(".xterm-rows")).to_contain_text(".git")
    page.screenshot(path="fin.png")
