import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from screenshot_maker.server import CodeServer


def run():
    with (
        tempfile.TemporaryDirectory() as tmp_path,
        CodeServer() as server,
        sync_playwright() as p,
    ):
        desktop = Path(tmp_path) / "home" / "student" / "Desktop"
        desktop.mkdir(parents=True)
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        try:
            page.goto(f"{server.url}/?folder={desktop}")

            # Open and name folder
            page.get_by_role("menuitem", name="Application Menu").click()
            page.get_by_role("menuitem", name="File", exact=True).click()
            page.get_by_role("menuitem", name="Open Folder...").click()
            folder_path = page.get_by_role("textbox", name="Folder path")
            folder_path.fill(f"{desktop}/test_repo")
            page.get_by_role("button", name="OK").click()  # "create new folder"
            page.get_by_role("button", name="OK").click()  # "are you sure?"
            page.wait_for_url("**/test_repo")

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
            page.locator("a").filter(has_text="Defines template").wait_for()

            # Look through files and take a screenshot
            page.keyboard.press("Control+Shift+`")
            page.locator(".xterm-link-layer").wait_for()
            page.get_by_role("textbox", name="Terminal").press_sequentially("ls -a\n")
            page.screenshot(path="stepfin.png")
        finally:
            context.tracing.stop(path="trace.zip")


if __name__ == "__main__":
    run()
