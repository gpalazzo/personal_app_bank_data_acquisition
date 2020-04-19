from env_var_handler.env_var_loader import load_credentials, load_config
from logs.logs_generator import LogsClient
from pathlib import Path
import os
from src.clients.chrome_client import ChromeClient
from typing import List
from time import sleep
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


file_name = os.path.basename(__file__)
project_dir = Path(__file__).resolve().parents[3]


class MagnetisWrapper:

    def __init__(self,
                 log_run_uuid,
                 log_output_file,
                 options: List = ["--headless",
                                 {"profile.managed_default_content_settings.images": 2}]):

        # load credentials and configs as env variables
        load_credentials(), load_config()
        self.url = os.getenv("magnetis_url")
        self.username = os.getenv("magnetis_username")
        self.password = os.getenv("magnetis_password")
        self.log_run_uuid = log_run_uuid
        self.log_output_file = log_output_file
        self.chrome = ChromeClient(log_run_uuid=log_run_uuid,
                                   log_output_file=log_output_file,
                                   _options=options)\
                                    .client

    def find_element(self, find_method: str, path_to_elem: str, more_than_1_elem: bool = False) -> WebElement:

        log_client = LogsClient(output_file=self.log_output_file,
                                project_dir=project_dir,
                                file_name=file_name,
                                log_run_uuid=self.log_run_uuid)

        try:

            log_client.set_msg(log_type="info",
                               log_msg=f"trying to reach element by {find_method} method at path: {path_to_elem}")

            if more_than_1_elem:

                if find_method == "class":

                    web_elem = self.chrome.find_elements_by_class_name(name=path_to_elem)

            else:

                if find_method == "xpath":

                    web_elem = self.chrome.find_element_by_xpath(xpath=path_to_elem)

                elif find_method == "class":

                    web_elem = self.chrome.find_element_by_class_name(name=path_to_elem)

            log_client.set_msg(log_type="info",
                               log_msg="element was reached successfully")

            sleep(0.1)

            return web_elem

        except NoSuchElementException:

            log_client.set_msg(log_type="error",
                               log_msg=f"error while trying to find elem at path: {path_to_elem}")

        except Exception as e:

            log_client.set_msg(log_type="error",
                               log_msg=f"the following error occurred with args: {e.args}")

    def action_on_elem(self, web_elem: WebElement, action: str, content: str = ""):

        log_client = LogsClient(output_file=self.log_output_file,
                                project_dir=project_dir,
                                file_name=file_name,
                                log_run_uuid=self.log_run_uuid)

        log_client.set_msg(log_type="info",
                           log_msg=f"action: {action} on web element: {web_elem}")

        try:

            if action == "click":

                web_elem.click()

            elif action == "send_keys":

                web_elem.send_keys(content)

            sleep(2)

        except NoSuchElementException:

            log_client.set_msg(log_type="error",
                               log_msg=f"error while trying to perform action: {action} at web element: {web_elem}")

        except Exception as e:

            log_client.set_msg(log_type="error",
                               log_msg=f"the following error occurred with args: {e.args}")

    def get_initial_page(self):

        log_client = LogsClient(output_file=self.log_output_file,
                                project_dir=project_dir,
                                file_name=file_name,
                                log_run_uuid=self.log_run_uuid)

        try:
            # delete cookies and go to defined url
            log_client.set_msg(log_type="info",
                               log_msg="deleting browser cookies")

            self.chrome.delete_all_cookies()

            sleep(2)

            log_client.set_msg(log_type="info",
                               log_msg=f"going to url: {self.url}")

            self.chrome.get(self.url)

            sleep(5)

            xpath = '//*[@id="user_email"]'

            username_elem = self.find_element(find_method="xpath",
                                              path_to_elem=xpath)

            self.action_on_elem(web_elem=username_elem,
                                action="send_keys",
                                content=self.username)

            sleep(5)

            xpath = '//*[@id="user_password"]'

            password_elem = self.find_element(find_method="xpath",
                                              path_to_elem=xpath)

            self.action_on_elem(web_elem=password_elem,
                                action="send_keys",
                                content=self.password)

            # login after filling in the password
            loggin_btn_xpath = '//*[@id="new_user"]/input[2]'

            login_btn = self.find_element(find_method="xpath",
                                          path_to_elem=loggin_btn_xpath)

            log_client.set_msg(log_type="info",
                               log_msg="logging in")

            self.action_on_elem(web_elem=login_btn,
                                action="click")

            sleep(5)

            return self.chrome

        except Exception as e:

            log_client.set_msg(log_type="error",
                               log_msg=f"the following error occurred with args: {e.args}")

        # finally:
        #
        #     assert False, "breaking code execution, see log file to track error"
