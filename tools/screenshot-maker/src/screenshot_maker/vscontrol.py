from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    page.goto("http://localhost:3000/")
    # Open and name folder
    page.get_by_role("menu", name="Application Menu").click()
    page.get_by_role("menuitem", name="Open Folder...").click()
    page.get_by_role("textbox", name="input", exact=True).fill(
        "/Users/henry/test_repo"
    )  # specific to me
    page.get_by_role("textbox", name="input", exact=True).press("Enter")
    page.get_by_role("textbox", name="input", exact=True).press("Enter")

    # Init Repo (with trusted mode too)
    page.get_by_role("tab", name="Source Control (⌃⇧G)").click()
    page.get_by_role("button", name="Restricted Mode: Some").click()
    page.get_by_role("button", name="Trust", exact=True).click()
    page.get_by_role("button", name="Close Modal Editor (Escape)").click()
    page.get_by_role("button", name="Initialize Repository").click()

    # Make new file and fill with Gucamole
    page.get_by_label("Explorer (⇧⌘E)").first.click()
    page.get_by_role("button", name="New File...", exact=True).click()
    page.get_by_role("textbox", name="Type file name. Press Enter").fill("guacamole.md")
    page.get_by_role("textbox", name="Type file name. Press Enter").press("Enter")
    page.get_by_role("textbox", name="guacamole.md").type("# Guacomole")
    page.get_by_role("textbox", name="guacamole.md").press("Enter")
    page.get_by_role("textbox", name="guacamole.md").type("## Ingredients")
    page.get_by_role("textbox", name="guacamole.md").press("Enter")
    page.get_by_role("textbox", name="guacamole.md").press("Enter")
    page.get_by_role("textbox", name="guacamole.md").type("## Instructions")

    # Commit changes
    page.get_by_role("tab", name="Source Control (⌃⇧G) - 1").click()
    page.get_by_role("button", name="Stage Changes").click()
    page.get_by_role("textbox", name="Message (⌘Enter to commit on").click()
    page.get_by_role("button", name='Commit Changes on "main"').click()

    # look through files and take a screenshot
    page.get_by_role("menuitem", name="New Terminal ⇧⌘C").click()
    page.get_by_role("textbox", name="Terminal 1, zsh Run the").fill("ls")
    page.get_by_role("textbox", name="Terminal 1, zsh Run the").press("q")
    page.get_by_role("textbox", name="Terminal 1, zsh Run the").press("ControlOrMeta+j")
    page.screenshot(path="example.png")
