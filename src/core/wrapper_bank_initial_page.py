from src.clients.chrome_client import ChromeClient
from time import sleep
from typing import List
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import os
from env_var_handler.env_var_loader import load_credentials, load_config


class BankWrapper:
    """Class that encapsulates the process of inserting env_var_handler into bank web page.
    """

    def __init__(self, options: List = ["--headless",
                                        {"profile.managed_default_content_settings.images": 2}]):
        """Creates instance of BankWrapper class with needed objects to login into bank web page.
        Args:
            options: options to be inserted into ChromeOptions class. Defaults to ["--headless",
                                                                {"profile.managed_default_content_settings.images": 2}]
        """
        # load credentials and configs as env variables
        load_credentials(), load_config()
        self.url = os.getenv("bank_url")
        self.agency = os.getenv("bank_agency")
        self.account = os.getenv("bank_account")
        self.password = os.getenv("bank_password")
        self.chrome = ChromeClient(_options=options).client

    def find_element(self, find_method: str, path_to_elem: str, more_than_1_elem: bool = False) -> WebElement:

        try:
            if more_than_1_elem:
                if find_method == "class":
                    return self.chrome.find_elements_by_class_name(name=path_to_elem)

            else:
                if find_method == "xpath":
                    return self.chrome.find_element_by_xpath(xpath=path_to_elem)
                elif find_method == "class":
                    return self.chrome.find_element_by_class_name(name=path_to_elem)

            sleep(0.1)

        except NoSuchElementException as e:
            print(f"Error while trying to find elem at path: {path_to_elem}")
            print(f"Error args: {e.args}")

    @staticmethod
    def action_on_elem(web_elem: WebElement, action: str, content: str = ""):

        try:

            if action == "click":
                web_elem.click()
            elif action == "send_keys":
                web_elem.send_keys(content)

            sleep(2)

        except NoSuchElementException as e:
            print(f"It's not possible to perform the action {action} on element {web_elem}")
            print(f"Error args: {e.args}")

    def get_initial_page(self):

        try:

            # delete cookies and go to defined url
            self.chrome.delete_all_cookies()
            sleep(2)
            self.chrome.get(self.url)
            sleep(4)

            # get agency text box
            agency = self.find_element(find_method="xpath",
                                       path_to_elem='//*[@id="cooperativa"]')

            sleep(2)
            # fill in agency
            print("Filling agency...")
            self.action_on_elem(web_elem=agency,
                                action="send_keys",
                                content=self.agency)

            sleep(2)

            # get account text box
            account = self.find_element(find_method="xpath",
                                        path_to_elem='//*[@id="conta"]')

            # fill in account
            print("Filling account...")
            self.action_on_elem(web_elem=account,
                                action="send_keys",
                                content=self.account)
            sleep(2)

            # loop over password length
            for i, character in enumerate(self.password, 1):

                numbered_btns = self.find_element(find_method="class",
                                                  path_to_elem="tecla",
                                                  more_than_1_elem=True)

                print(f"Filling character {i} of the password...")

                # when there's match between password character and web page character, then click on it
                for number in numbered_btns:
                    if number.text == character:
                        self.action_on_elem(web_elem=number,
                                            action="click")

            # login after filling in the password
            login_btn = self.find_element(find_method="xpath",
                                          path_to_elem='//*[@id="buttons"]/input[1]')
            print("Logging in...")
            self.action_on_elem(web_elem=login_btn,
                                action="click")
            sleep(2)

        except Exception as e:
            print(f"Error args: {e.args}")
            self.chrome.quit()

        # return chrome with web page authenticated
        return self.chrome
