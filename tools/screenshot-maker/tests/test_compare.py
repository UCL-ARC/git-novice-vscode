from pathlib import Path

import pytest
from PIL import Image, ImageColor

from screenshot_maker.compare import compare_screenshots


@pytest.mark.parametrize(
    "first, second, existing, updated, kept",
    [
        ("red", "red", "black", ["screenshot.png"], "red"),
        ("red", "red", None, ["screenshot.png"], "red"),
        ("red", "blue", "black", [], "black"),
        ("black", "black", "black", [], "black"),
    ],
    ids=["runs agree on a change", "new screenshot", "runs disagree", "nothing changed"],
)
def test_compare_screenshots(
    tmp_path: Path,
    first: str,
    second: str,
    existing: str | None,
    updated: list[str],
    kept: str,
) -> None:
    colours = {"first": first, "second": second, "existing": existing}
    for folder, colour in colours.items():
        (tmp_path / folder).mkdir()
        if colour:
            Image.new("RGB", (1, 1), colour).save(tmp_path / folder / "screenshot.png")

    assert compare_screenshots(*(tmp_path / folder for folder in colours)) == updated
    with Image.open(tmp_path / "existing" / "screenshot.png") as image:
        assert image.getpixel((0, 0)) == ImageColor.getrgb(kept)
