"""
Configuration for pytest
"""
from typing import Any, Generator

import pytest

from starlette.testclient import TestClient


from app.main import get_application

app = get_application()



@pytest.fixture(scope="function")
def client() -> Generator[TestClient, Any, None]:
    """
    Creates a test client for http requests
    :return:
    """

    with TestClient(app) as test_client:
        yield test_client
        