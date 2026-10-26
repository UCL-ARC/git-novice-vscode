import os
import signal
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from loguru import logger

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SERVER_DATA_DIR = _PROJECT_ROOT / "server-data"


@dataclass
class CodeServer:
    """
    A context manager class that handles the Visual Studio Code server instance.

    If the server is already running on the specified host and port: don't start a new one, don't
    take ownership. If no server is running: start one and stop when the context manager exits.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    timeout_seconds: float = 30
    process: subprocess.Popen | None = field(default=None, init=False)
    code_binary: str = os.getenv("CODE_BIN", "code")
    env: dict[str, str] = field(default_factory=dict)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def _is_reachable(self):
        try:
            with urlopen(self.url, timeout=1):
                if self.process:
                    logger.info(f"VS Code server ready at {self.url} with ID {self.process.pid}")
                else:
                    logger.info(f"VS Code server already ready at {self.url}")
                return True
        except OSError, URLError, TimeoutError:
            return False

    def start(self):
        if self._is_reachable():
            return self

        logger.info(f"Starting VS Code server {self.url}...")
        self.process = subprocess.Popen(
            [
                self.code_binary,
                "serve-web",
                "--host",
                self.host,
                "--port",
                str(self.port),
                "--without-connection-token",
                "--accept-server-license-terms",
                "--disable-telemetry",
                "--server-data-dir",
                str(_SERVER_DATA_DIR),
            ],
            stdout=subprocess.DEVNULL,
            env={**os.environ, **self.env},
            # Own process group, so stop() can kill the child processes `code` spawns.
            # POSIX only (macOS/Linux): Windows isn't supported.
            start_new_session=True,
        )

        return self._wait_until_ready()

    def _wait_until_ready(self):
        if not self.process:
            logger.warning("No process to wait for. The server may already be running.")
            return self

        timeout_deadline = time.monotonic() + self.timeout_seconds
        while time.monotonic() < timeout_deadline:
            if self._is_reachable():
                break
            if self.process.poll() is not None:
                raise RuntimeError("The VS Code server exited before becoming ready")
            time.sleep(0.2)
        else:
            self.stop()
            raise TimeoutError(
                f"VS Code server did not become ready at {self.url} after {self.timeout_seconds} seconds"
            )

        return self

    def _signal_group(self, sig: signal.Signals):
        if not self.process:
            logger.warning("No process to signal. The server may already be stopped.")
            return
        try:
            # The group id is equal to the launcher's pid.
            os.killpg(self.process.pid, sig)
        except ProcessLookupError:
            logger.warning("Process group not found. The server may already be stopped.")

    def stop(self):
        if self.process is None or self.process.poll() is not None:
            logger.warning("No process. The server may already be stopped.")
            return

        logger.info("Stopping VS Code web server")
        self._signal_group(signal.SIGTERM)
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._signal_group(signal.SIGKILL)
            self.process.wait()
        self.process = None
        logger.info("Terminated")

    # Enter and exit methods to make this class into a context manager.

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
