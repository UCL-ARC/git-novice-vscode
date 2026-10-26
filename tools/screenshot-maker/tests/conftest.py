import pytest

from screenshot_maker.server import CodeServer


@pytest.fixture
def vscode_page_and_path(tmp_path, page):
    # A playwright.Page fixture for testing playwright interaction functions with a new clean vscode server.
    # Some tests will also want to check things are created at the path.
    with CodeServer() as server:
        page.goto(f"{server.url}/?folder={tmp_path}")
        yield page, tmp_path


@pytest.fixture
def vscode_page(vscode_page_and_path):
    page, _ = vscode_page_and_path
    yield page
