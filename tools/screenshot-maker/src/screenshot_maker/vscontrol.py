from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False, slow_mo=200)
    page = browser.new_page()
    page.goto("http://localhost:3000")

    # Open and name folder
    page.get_by_role("menuitem", name="Application Menu").click()
    page.get_by_role("menuitem", name="File", exact=True).click()
    page.get_by_role("menuitem", name="Open Folder...").click()
    folder_path = page.get_by_role("textbox", name="Folder path")
    folder_path.type("Desktop/test_repo")
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
    page.get_by_role("tab", name="Terminal (⌃`)").click()
    page.get_by_role("textbox", name="Terminal").press_sequentially("ls -a")
    page.get_by_role("textbox", name="Terminal").press("Enter")
    page.screenshot(path="example.png")
