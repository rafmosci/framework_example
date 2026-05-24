import pytest

@pytest.fixture(scope="session")
def base_url():
    """Return URL for API tests"""

    return "https://dummyjson.com"