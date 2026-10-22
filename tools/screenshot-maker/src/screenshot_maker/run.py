import re
import tempfile
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from screenshot_maker.server import CodeServer


def run():
    with (
        tempfile.TemporaryDirectory() as tmp_path,
        CodeServer() as server,
        sync_playwright() as p,
    ):
        desktop = Path(tmp_path) / "home" / "student" / "Desktop"
        desktop = Path(tmp_path) / "home" / "student" / "Desktop"
        desktop.mkdir(parents=True)
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(f"{server.url}/?folder={desktop}")

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

        # Commit changes
        page.keyboard.press("Control+Shift+G")
        page.get_by_role("treeitem", name="Changes", exact=True).hover()
        page.get_by_role("button", name="Stage All Changes").click()
        page.get_by_role("treeitem", name="Staged Changes").wait_for()
        message = page.get_by_role("textbox", name="Message")
        message.press_sequentially("Defines template")
        message.press("ControlOrMeta+Enter")

        # Look through files and take a screenshot
        page.keyboard.press("Control+Shift+`")
        terminal = page.get_by_role("textbox", name=re.compile(r"^Terminal \d+, "))
        terminal.press_sequentially("ls -a\n")
        expect(page.locator(".codicon-terminal-decoration-success")).to_be_visible(timeout=20_000)
        page.screenshot(path="example.png")


if __name__ == "__main__":
    run()
