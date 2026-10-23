import pytest
from playwright.sync_api import sync_playwright

from screenshot_maker.server import CodeServer


@pytest.fixture
def vscode_page(tmp_path):
    # A playwright.Page fixture for testing playwright interaction functions with a new clean vscode server.
    with CodeServer() as server, sync_playwright() as playwright_context:
        page = playwright_context.firefox.launch(headless=True).new_page()
        page.goto(f"{server.url}/?folder={tmp_path}")

        yield page
