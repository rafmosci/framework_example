import pytest

@pytest.fixture(scope="session")
def base_url():
    """Return URL for API tests"""

    return "https://dummyjson.com"

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Generate test report for executed test cases
    """
    outcome = yield
    report = outcome.get_result()

    description = item.function.__doc__ if item.function.__doc__ else "Empty description"
    report.description = description

    if report.when == "call" and report.failed:
        fixture_names = ["response", "shared_response"]
        for name in fixture_names:
            if name in item.funcargs:
                res = item.funcargs[name]
                if hasattr(res, 'status_code'):
                    print(f"Test failed! Response details:")
                    print(f"\n[DEBUG] URL: {res.url} | Status: {res.status_code}")
                    print(f"\n-> Response Body: {res.text}")
                    break