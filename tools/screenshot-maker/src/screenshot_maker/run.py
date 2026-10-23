import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from .episodes import EPISODES
from .server import CodeServer


def _make_student_desktop(tmp_path: str) -> Path:
    """Create a fake 'Desktop' folder: students should work on their desktops."""
    desktop = Path(tmp_path) / "home" / "student" / "Desktop"
    desktop.mkdir(parents=True)
    return desktop


def run() -> None:
    with (
        tempfile.TemporaryDirectory() as tmp_path,
        CodeServer() as server,
        sync_playwright() as playwright_context,
    ):
        desktop = _make_student_desktop(tmp_path)
        browser = playwright_context.firefox.launch()
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.goto(f"{server.url}/?folder={desktop}")

        for episode in EPISODES:
            episode(page, desktop)


if __name__ == "__main__":
    run()
