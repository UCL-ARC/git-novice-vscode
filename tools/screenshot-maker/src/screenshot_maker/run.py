import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

from .episodes import EPISODES
from .server import CodeServer

FIGURES = Path(__file__).parents[4] / "episodes" / "fig"


def _make_student_desktop(tmp_path: str) -> Path:
    """Create a fake 'Desktop' folder: students should work on their desktops."""
    desktop = Path(tmp_path) / "home" / "student" / "Desktop"
    desktop.mkdir(parents=True)
    return desktop


def run(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    # bash is still writing session files into the fake home as the server shuts down.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_path:
        desktop = _make_student_desktop(tmp_path)
        student_env = {
            "HOME": str(desktop.parent),
            "GIT_CONFIG_GLOBAL": str(desktop.parent / ".gitconfig"),
            "VSCODE_CLI_DATA_DIR": str(Path.home() / ".vscode" / "cli"),
        }
        with (
            CodeServer(additional_env=student_env) as server,
            sync_playwright() as playwright_context,
        ):
            browser = playwright_context.firefox.launch()
            context = browser.new_context()
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            page = context.new_page()
            page.goto(f"{server.url}/?folder={desktop}")

            for episode in EPISODES:
                episode(page, desktop, output)


if __name__ == "__main__":
    run(output=FIGURES)
