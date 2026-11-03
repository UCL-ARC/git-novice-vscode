from pathlib import Path

from PIL import Image

from screenshot_maker.compare import compare_screenshots


def test_compare_screenshots(tmp_path: Path) -> None:
    """
    Check compare_screenshots copies a new screenshot over an existing one of a different
    size, then copies nothing when the same screenshot comes in again.
    """
    new_screenshots = tmp_path / "new"
    existing_screenshots = tmp_path / "existing"
    new_screenshots.mkdir()
    existing_screenshots.mkdir()
    Image.new("RGB", (1, 1)).save(existing_screenshots / "screenshot.png")
    Image.new("RGB", (20, 20)).save(new_screenshots / "screenshot.png")

    assert compare_screenshots(new_screenshots, existing_screenshots) == ["screenshot.png"]
    with Image.open(existing_screenshots / "screenshot.png") as image:
        assert image.size == (20, 20)
    assert compare_screenshots(new_screenshots, existing_screenshots) == []
