"""David's example."""

from pathlib import Path

from playwright.sync_api import Page, expect

from ..ui import commit_changes


def example(page: Page, desktop: Path, output: Path) -> None:

    # Open and name folder
    page.get_by_role("menuitem", name="Application Menu").click()
    page.get_by_role("menuitem", name="File", exact=True).click()
    page.get_by_role("menuitem", name="Open Folder...").click()
    folder_path = page.get_by_role("textbox", name="Folder path")
    folder_path.type(f"{desktop}/test_repo")
    folder_path.press("Enter")
    page.keyboard.press("Enter")

    # Trust folder and Init repo
    page.get_by_role("button", name="Restricted Mode: Some").click()
    page.get_by_role("button", name="Trust", exact=True).click()
    page.get_by_role("button", name="Close Modal Editor (Escape)").click()
    page.keyboard.press("Control+Shift+G")
    page.get_by_role("button", name="Initialize Repository").click()

    # Make new file and fill with Gucamole
    page.keyboard.press("ControlOrMeta+Shift+E")
    page.get_by_role("button", name="New File...", exact=True).click()
    file_name = page.get_by_role("textbox", name="Type file name")
    file_name.fill("guacamole.md")
    file_name.press("Enter")
    editor = page.get_by_role("textbox", name="guacamole.md")
    editor.press_sequentially("# Guacamole\n## Ingredients\n\n## Instructions\n")
    editor.press("ControlOrMeta+s")

    commit_changes(page, "Defines template")

    # Look through files and take a screenshot
    page.keyboard.press("Control+Shift+`")
    prompts = page.locator(".terminal-command-decoration")
    expect(prompts).to_have_count(1, timeout=30_000)
    page.get_by_role("textbox", name="Terminal").press_sequentially("ls -a\n")
    expect(prompts).to_have_count(2)
    page.screenshot(path=output / "example.png")
