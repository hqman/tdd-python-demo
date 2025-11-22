"""Test project structure and dependencies setup."""
import importlib.util


def test_youtube_api_module_exists():
    """Test that youtube_api module can be imported."""
    spec = importlib.util.find_spec("tdd_python_demo.youtube_api")
    assert spec is not None, "youtube_api module should exist"
