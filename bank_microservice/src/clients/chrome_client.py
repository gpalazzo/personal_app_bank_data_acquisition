from selenium import webdriver
from typing import List
from selenium.webdriver import ChromeOptions
from bank_microservice import setup
from logs_microservice.logs import LogHandler


class ChromeClient:
    """Class to simulate Google Chrome browser through selenium.
    """

    def __init__(self, _options: List = []):
        """Creates instance of Google Chrome browser.
        Args:
            _options: list containing options to be inserted in the ChromeOptions class. Defaults to []
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.options = self._set_chrome_options(_options)
        self.client = webdriver.Chrome(list(setup.__path__)[0] + "/chromedriver",
                                       chrome_options=self.options)

    @staticmethod
    def _set_chrome_options(options: List) -> ChromeOptions:
        """Static method to create a ChromeOptions class with options.
        Args:
            options: list of options as defined in __init___ method
        Returns:
            instance of ChromeOptions with options defined in options parameter
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        chrome_options = ChromeOptions()

        for option in options:
            if isinstance(option, dict):
                chrome_options.add_experimental_option("prefs", option)
            else:
                chrome_options.add_argument(option)

        return chrome_options
