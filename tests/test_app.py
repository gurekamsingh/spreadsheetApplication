"""Test the Flask application."""

from backend.app import create_app


def test_app_creation():
    """Test that the Flask application can be created."""
    app = create_app()
    assert app is not None
    assert not app.config["TESTING"]


def test_app_testing_mode():
    """Test that the Flask application can be created in testing mode."""
    app = create_app(testing=True)
    assert app is not None
    assert app.config["TESTING"]
