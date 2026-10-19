
import pytest

from screenshot_maker.server import CodeServer


def test_server_starts():
    with CodeServer() as cs:
        assert cs._is_reachable()
        assert cs.url == "http://127.0.0.1:8000", "The server isn't at the default URL"


@pytest.mark.skip("Can't stop the server: vscode survives if the process is killed!")
def test_server_stops():
    server = CodeServer(port=8919)
    server.start()
    assert server._is_reachable()

    server.stop()

    assert not server._is_reachable(), "Should not be reachable after stopping"


def test_server_doesnt_respawn():
    """
    Creating a second instance with the same port shouldn't start a new process.

    Even if `start` is called: if a server is already running on that port, it
    should just return without starting a new process.
    """
    with CodeServer(port=9876):
        second_instance = CodeServer(port=9876)
        assert second_instance._is_reachable(), "Second instance should see the server."
        assert second_instance.process is None, "Shouldn't have started second process."

        second_instance.start()  # should do nothing
        assert second_instance.process is None
