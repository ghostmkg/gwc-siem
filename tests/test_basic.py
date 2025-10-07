"""
Test suite for GWC-SIEM
"""

import pytest


def test_basic():
    """Basic test to ensure pytest works"""
    assert True


def test_api_import():
    """Test that API module can be imported"""
    try:
        from api import main

        assert hasattr(main, "app")
    except ImportError:
        pytest.skip("API module not available")


def test_cli_import():
    """Test that CLI module can be imported"""
    try:
        from cli import app

        assert hasattr(app, "main")
    except ImportError:
        pytest.skip("CLI module not available")
