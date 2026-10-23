import subprocess
from pathlib import Path

from screenshot_maker.cli import _setup_parser


def test_import_smoke():
    import screenshot_maker  # noqa: F401


def test_entrypoint_is_available_to_uv_run():
    uv_run = subprocess.run(
        ["uv", "run"],
        capture_output=True,
        text=True,
        check=False,  # uv run with no args returns 2 but helpfully lists all available entrypoints and tools
    )

    assert "screenshot-maker" in uv_run.stdout


def test_help():
    # Make sure the CLI is working and gives helpful help.
    uv_run = subprocess.run(
        ["uv", "run", "screenshot-maker", "--help"],
        capture_output=True,
        text=True,
        check=False,  # --help returns 0
    )

    assert "usage:" in uv_run.stdout
    assert "Git Novice Carpentries" in uv_run.stdout
    assert "--output" in uv_run.stdout


def test_parsing():
    parser = _setup_parser()
    args = parser.parse_args(["--output", "my_screenshots"])
    assert args.output == Path("my_screenshots")
