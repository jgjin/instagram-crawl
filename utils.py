"""Utils for parsing IG."""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_options(
        headless,
):
    """Set Firefox options."""
    options = Options()
    options.headless = headless

    return options


def get_driver(
        headless=True,
):
    """Get Firefox driver."""
    driver = webdriver.Firefox(options=get_options(headless))
    return driver
