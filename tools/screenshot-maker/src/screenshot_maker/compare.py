from pathlib import Path

from PIL import Image, ImageChops


def compare_screenshots(new_screenshots: Path, existing_screenshots: Path) -> None:
    # for sshot in new_screenshots:
    #     x = Path(sshot)
    #     y = Path(existing_screenshots) / x.name
    #     if not y.is_file():
    #         raise FileNotFoundError(f"Expected screenshot {y} does not exist.")
    #     if _images_differ(x, y):
    #         # copy over / update
    #     else:
    #         continue
    pass


def _images_differ(a: Path, b: Path) -> bool:
    """Compare two images and return True if they are different, False if the same."""
    with Image.open(a) as imagea, Image.open(b) as imageb:
        return ImageChops.difference(imagea, imageb).getbbox() is not None
