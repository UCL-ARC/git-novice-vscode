from selenium import webdriver

from .episodes import episode_1
from .server import CodeServer


def run():
    print("Running screenshot maker...")
    with CodeServer() as cs:
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
        driver.get(cs.url)
        episode_1(driver)


if __name__ == "__main__":
    run()
