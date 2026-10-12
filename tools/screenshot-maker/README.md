# Screenshot maker

This is a very small python package that uses [`selenium`](https://pypi.org/project/selenium/) to regenerate the screenshots of Visual Studio Code for this lesson.

You can install it with `uv`.
From the root of this repository, run:

```bash
uv sync --project tools/screenshot-maker
source tools/screenshot-maker/.venv/bin/activate
```

Then you can run it with:

```bash
uv run screenshot-maker
```

or

```bash
python -m screenshot_maker.run
```

Which is a calls the `run()` function in `screenshot_maker/run.py` (the code entry point of this package).
