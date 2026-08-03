import pytest
from selenium import webdriver


# Step 48

@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# Step 41

@pytest.fixture(scope="function")
def driver(request):
    driver = webdriver.Chrome()

    request.node.driver = driver

    yield driver

    driver.quit()


# Step 46

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)

        if driver:
            test_name = item.name
            driver.save_screenshot(
                f"images/{test_name}_failure.png"
            )