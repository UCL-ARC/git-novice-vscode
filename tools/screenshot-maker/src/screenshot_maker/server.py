import subprocess
import time
from dataclasses import dataclass, field
from urllib.error import URLError
from urllib.request import urlopen

from loguru import logger


@dataclass
class CodeServer:
    """A context manager class to manage either an existing VS Code web server or start a new one if needed."""

    host: str = "127.0.0.1"
    port: int = 8000
    timeout_seconds: float = 30
    process: subprocess.Popen | None = field(default=None, init=False)

    @property
    def url(self):
        return f"http://{self.host}:{self.port}"

    def _is_ready(self):
        try:
            with urlopen(self.url, timeout=1):
                if self.process:
                    logger.info(
                        f"VS Code web server is ready at {self.url} with PID {self.process.pid}"
                    )
                else:
                    logger.info(f"VS Code web server is already ready at {self.url}")
                return True
        except OSError, URLError, TimeoutError:
            return False

    def start(self):
        if self._is_ready():
            return self

        logger.info(f"Starting VS Code web server at {self.url}...")
        self.process = subprocess.Popen(
            [
                "code",
                "serve-web",
                "--host",
                self.host,
                "--port",
                str(self.port),
                "--without-connection-token",
                "--accept-server-license-terms",
            ],
            stdout=subprocess.DEVNULL,
        )

        return self._wait_until_ready()

    def _wait_until_ready(self):
        if not self.process:
            logger.warning("No process to wait for. The server may already be running.")
            return self

        deadline = time.monotonic() + self.timeout_seconds
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise RuntimeError(
                    "The VS Code web server exited before becoming ready"
                )
            if self._is_ready():
                break
            time.sleep(0.2)
        else:
            self.stop()
            raise TimeoutError(
                f"VS Code web server did not become ready at {self.url} after {self.timeout_seconds} seconds"
            )

        return self

    def stop(self):
        if self.process is None or self.process.poll() is not None:
            return

        logger.info("Stopping VS Code web server")
        self.process.terminate()

        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()

    # Enter and exit methods to make this class into a context manager.

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
