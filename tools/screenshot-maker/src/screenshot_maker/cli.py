"""A command-line entry point for the screenshot maker."""

import argparse
from pathlib import Path

from .run import run


def _setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="screenshot-maker",
        description="Screenshot making tool for the Git Novice Carpentries lesson using Visual Studio Code.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("./screenshots"),
        help="Output directory to save screenshots",
    )
    return parser


def cli() -> int:
    """The command-line interface wrapper for the `run` function."""
    parser = _setup_parser()
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    run(output=args.output)
    return 0
