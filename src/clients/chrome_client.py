from selenium import webdriver
from typing import List
from selenium.webdriver import ChromeOptions
import setup
from pathlib import Path
import os
from logs.logs_generator import LogsClient


project_dir = Path(__file__).resolve().parents[2]
file_name = os.path.basename(__file__)


class ChromeClient:
    """Class to simulate Google Chrome browser through selenium.
    """

    def __init__(self,
                 log_run_uuid,
                 log_output_file,
                 _options: List = []):
        """Creates instance of Google Chrome browser.
        Args:
            _options: list containing options to be inserted in the ChromeOptions class. Defaults to []
        """
        self.log_run_uuid = log_run_uuid
        self.log_output_file = log_output_file
        self.options = self._set_chrome_options(_options)
        self.client = webdriver.Chrome(list(setup.__path__)[0] + "/chromedriver",
                                       chrome_options=self.options)

    def _set_chrome_options(self, options: List) -> ChromeOptions:
        """Static method to create a ChromeOptions class with options.
        Args:
            options: list of options as defined in __init___ method
        Returns:
            instance of ChromeOptions with options defined in options parameter
        """
        log_client = LogsClient(output_file=self.log_output_file,
                                project_dir=project_dir,
                                file_name=file_name,
                                log_run_uuid=self.log_run_uuid)

        log_client.set_msg(log_type="info",
                           log_msg="setting chrome options")

        try:

            chrome_options = ChromeOptions()

            for option in options:
                if isinstance(option, dict):
                    chrome_options.add_experimental_option("prefs", option)
                else:
                    chrome_options.add_argument(option)

            return chrome_options

        except Exception as e:

            log_client.set_msg(log_type="error",
                               log_msg=f"the following error occurred with args: {e.args}")

            assert False, "breaking code execution, see log file to track error"
