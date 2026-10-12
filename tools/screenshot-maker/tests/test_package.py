import subprocess


def test_import():
    import screenshot_maker  # noqa: F401


def test_entrypoint_is_available_to_uv_run():
    uv_run = subprocess.run(
        ["uv", "run"],
        capture_output=True,
        text=True,
        check=False,  # uv run with no args returns 2 but helpfully lists all available entrypoints and tools
    )

    assert "screenshot-maker" in uv_run.stdout
