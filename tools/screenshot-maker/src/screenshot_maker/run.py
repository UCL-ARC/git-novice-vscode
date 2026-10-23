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


def run(output: Path) -> None:
    with (
        tempfile.TemporaryDirectory() as tmp_path,
        CodeServer() as server,
        sync_playwright() as playwright_context,
    ):
        desktop = _make_student_desktop(tmp_path)
        page = playwright_context.firefox.launch().new_page()
        page.goto(f"{server.url}/?folder={desktop}")

        for episode in EPISODES:
            episode(page, desktop, output)


if __name__ == "__main__":
    run(output=Path("./screenshots"))
