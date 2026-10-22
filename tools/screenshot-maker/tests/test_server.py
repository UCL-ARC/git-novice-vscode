from screenshot_maker.server import _SERVER_DATA_DIR, CodeServer


def test_server_starts():
    with CodeServer() as cs:
        assert cs._is_reachable()
        assert cs.url == "http://127.0.0.1:8000", "The server isn't at the default URL"


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


def test_globals_server_data_directory():
    assert _SERVER_DATA_DIR.exists(), "The server data dir should exist"
    assert _SERVER_DATA_DIR.is_dir(), "The server data dir should be a directory"
    assert (_SERVER_DATA_DIR / "data" / "Machine").is_dir(), "Settings directory should exist"
