"""
This module contains fixtures for the unit tests.
"""
import os
from unittest.mock import patch
import pytest


@pytest.fixture(autouse=True)
def mock_env_variables():
    """
    Fixture to create a Database instance for testing.
    """
    with patch.dict(os.environ, {
        'SQL_SERVER': 'localhost',
        'SQL_DATABASE': 'test_db',
        'SQL_USERNAME': 'test_user',
        'SQL_PASSWORD': 'test_password',
    }):
        yield
