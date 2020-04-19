from logs.logs_generator import LogsClient
import uuid
from time import sleep
from selenium.webdriver import Chrome
from pathlib import Path
import os
from typing import Dict, Any
import io
import json
from src.wrappers.magnetis_webpage_auth import MagnetisWrapper
from datetime import datetime
from src.clients.aws_s3_bucket import S3Bucket


project_dir = Path(__file__).resolve().parents[3]


log_client = LogsClient(output_file="magnetis_investments_balance.log",
                        project_dir=project_dir,
                        file_name=os.path.basename(__file__),
                        log_run_uuid=uuid.uuid4())


def create_json(file_path: str, data_dict: Dict[str, Any]):

    try:

        log_client.set_msg(log_type="info",
                           log_msg="creating json file")

        with io.open(os.path.join(file_path), 'w') as f:

            f.write(json.dumps(data_dict))

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def _get_chrome_authenticated():

    log_client.set_msg(log_type="info",
                       log_msg="getting chrome authenticated through bank wrapper")

    try:

        magnetis_initial_page = MagnetisWrapper(log_run_uuid=log_client.log_run_uuid,
                                                log_output_file=log_client.output_file,
                                                options=[])\
                                                .get_initial_page()

        return magnetis_initial_page

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def get_investments_balance(chrome: Chrome):

    try:

        xpath = '//*[@id="root"]/div/main/div[4]/div/div[1]/span'

        log_client.set_msg(log_type="info",
                           log_msg=f"trying to reach element at xpath: {xpath}")

        patrimony = chrome.find_element_by_xpath(xpath=xpath)
        sleep(2)

        log_client.set_msg(log_type="info",
                           log_msg="element was reached successfully")

        log_client.set_msg(log_type="info",
                           log_msg="parsing element text properties")

        patrimony_str = patrimony.text.replace(".", "").replace(",", ".")

        xpath = '//*[@id="root"]/div/main/div[4]/div/div[3]/span'

        log_client.set_msg(log_type="info",
                           log_msg=f"trying to reach element at xpath: {xpath}")

        gross_income = chrome.find_element_by_xpath(xpath=xpath)
        sleep(2)

        log_client.set_msg(log_type="info",
                           log_msg="element was reached successfully")

        log_client.set_msg(log_type="info",
                           log_msg="parsing element text properties")

        gross_income_str = gross_income.text.replace(".", "").replace(",", ".")

        xpath = '//*[@id="root"]/div/main/div[4]/div/div[2]/span'

        log_client.set_msg(log_type="info",
                           log_msg=f"trying to reach element at xpath: {xpath}")

        gross_return_pct = chrome.find_element_by_xpath(xpath=xpath)
        sleep(2)

        log_client.set_msg(log_type="info",
                           log_msg="element was reached successfully")

        log_client.set_msg(log_type="info",
                           log_msg="parsing element text properties")
        gross_return_pct_str = gross_return_pct.text.replace(".", "").replace(",", ".")

        return patrimony_str, gross_income_str, gross_return_pct_str

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        chrome.quit()


def main():

    log_client.set_msg(log_type="info",
                       log_msg="beginning of script")

    try:

        chrome = _get_chrome_authenticated()

        patrimony, gross_income, gross_return_pct = get_investments_balance(chrome=chrome)

        time_now = datetime.now()

        date_today = datetime.strftime(time_now, "%Y-%m-%d")

        file_path = project_dir / Path(f"output_files/magnetis_investments_balance_{date_today}.json")

        data_dict = {"action_timestamp": str(time_now),
                     "patrimony": patrimony,
                     "gross_income": gross_income,
                     "gross_return_pct": gross_return_pct}

        create_json(file_path=file_path, data_dict=data_dict)

        S3Bucket().upload_file(file_path=str(file_path))

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        log_client.set_msg(log_type="info",
                           log_msg="end of script")


if __name__ == "__main__":

    main()
