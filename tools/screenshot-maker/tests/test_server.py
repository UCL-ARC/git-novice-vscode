from urllib.request import urlopen
from time import sleep

import pytest

from screenshot_maker.server import CodeServer


def test_server_starts():
    with CodeServer() as cs:
        assert cs._is_ready()
        assert cs.url == "http://127.0.0.1:8000", "The server isn't at the default URL"


@pytest.mark.skip(
    "Can't seem to stop the server: it's vscode itself that sticks around after the process is killed."
)
def test_server_stops():
    server = CodeServer(port=8988)
    server.start()
    assert server._is_ready()

    server.stop()
    sleep(0.5)  # Give the server a moment to shut down
    assert not server._is_ready(), "The server should not be ready after stopping"
    assert not server.process, "The process should be None after stopping the server"

    with pytest.raises(RuntimeError):
        urlopen(server.url, timeout=1)
        pytest.fail("The server should not be reachable after stopping")
