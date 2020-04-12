from wrapper_bank_initial_page import BankWrapper
from datetime import datetime
import json
from pathlib import Path
import io
import os
from typing import Dict, Any
from src.clients.aws_s3_bucket import S3Bucket
import logging


project_dir = Path(__file__).resolve().parents[2]


def append_data_to_json(data_to_append: Dict[str, Any], file):

    logging.basicConfig(filename=f"{project_dir}/logs/logs_output/acc_balance.log",
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("beginning of function")

    try:

        logging.info("appending data to existing json file")

        new_file_content = {}

        for content in file:

            content_json = json.loads(content)

            for key, value in content_json.items():

                if isinstance(value, list):

                    value_list = value

                else:

                    value_list = [value]

                new_value = data_to_append[key]

                value_list.append(new_value)

                new_file_content[key] = value_list

        logging.info("ending of function")

        return new_file_content

    except Exception as e:

        logging.error(f"the following error occurred with args: {e.args}")


def create_json(file_path: str, data_dict: Dict[str, Any]):

    logging.basicConfig(filename=f"{project_dir}/logs/logs_output/acc_balance.log",
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("beginning of function")

    try:

        logging.info("creating json file")

        with io.open(os.path.join(file_path), 'w') as f:

            f.write(json.dumps(data_dict))

        logging.info("ending of function")

    except Exception as e:

        logging.error(f"the following error occurred with args: {e.args}")


def _get_chrome_authenticated():

    logging.basicConfig(filename=f"{project_dir}/logs/logs_output/acc_balance.log",
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("beginning of function")

    try:

        bank_initial_page = BankWrapper().get_initial_page()

        logging.info("ending of function")

        return bank_initial_page

    except Exception as e:

        logging.error(f"the following error occurred with args: {e.args}")


def get_acc_balance():

    logging.basicConfig(filename=f"{project_dir}/logs/logs_output/acc_balance.log",
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("beginning of function")

    try:

        chrome = _get_chrome_authenticated()

        acc_elem_xpath = '//*[@id="box_conteudo"]/table[1]/tbody/tr[1]/td[2]'

        logging.info(f"trying to reach acc balance element at xpath: {acc_elem_xpath}")

        acc_elem = chrome.find_element_by_xpath(acc_elem_xpath)

        logging.info("account balance element was reached successfully")

        acc_balance_str = acc_elem.text.replace(".", "").replace(",", ".")[:-1]

        chrome.quit()

        logging.info("ending of function")

        return float(acc_balance_str)

    except Exception as e:

        chrome.quit()

        logging.error(f"the following error occurred with args: {e.args}")


def main():

    logging.basicConfig(filename=f"{project_dir}/logs/logs_output/acc_balance.log",
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("beginning of function")

    try:

        acc_balance_float = get_acc_balance()

        time_now = datetime.now()

        date_today = datetime.strftime(time_now, "%Y-%m-%d")

        file_path = project_dir / Path(f"output_files/acc_balance_{date_today}.json")

        data_dict = {"action_timestamp": str(time_now),
                     "acc_balance": acc_balance_float,
                     "email_status": "not_sent"}

        if os.path.isfile(path=file_path) and os.access(file_path, os.R_OK):

            with open(file_path, 'r+') as f:

                file_content = append_data_to_json(data_dict, f)

                f.seek(0)

                f.truncate()

                json.dump(file_content, f)

        else:

            create_json(file_path=file_path, data_dict=data_dict)

        # S3Bucket().upload_file(file_path=str(file_path))

        logging.info("ending of function")

    except Exception as e:

        logging.error(f"the following error occurred with args: {e.args}")


if __name__ == "__main__":

    main()
