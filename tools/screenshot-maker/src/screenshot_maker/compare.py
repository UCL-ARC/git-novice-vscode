import shutil
from pathlib import Path

from loguru import logger
from PIL import Image, ImageChops


def compare_screenshots(new_screenshots: Path, existing_screenshots: Path) -> None:
    for new in sorted(new_screenshots.glob("*.png")):
        existing = existing_screenshots / new.name
        if not existing.is_file():
            raise FileNotFoundError(f"Expected screenshot {existing} does not exist.")
        if _images_differ(new, existing):
            logger.info(f"Updating {existing}")
            shutil.copy(new, existing)


def _images_differ(a: Path, b: Path) -> bool:
    """Compare two images and return True if they are different, False if the same."""
    with Image.open(a) as imagea, Image.open(b) as imageb:
        if imagea.size != imageb.size:
            logger.warning(f"Images have different sizes: {imagea.size} vs {imageb.size}")
            return True
        return ImageChops.difference(imagea, imageb).getbbox() is not None
