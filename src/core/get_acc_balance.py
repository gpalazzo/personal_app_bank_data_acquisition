from wrapper_bank_initial_page import BankWrapper
from datetime import datetime
import json
from pathlib import Path
import io
import os
from typing import Dict, Any
from src.clients.aws_s3_bucket import S3Bucket
from logs.logs_generator import LogsClient
import uuid


project_dir = Path(__file__).resolve().parents[2]
file_name = os.path.basename(__file__)
log_run_uuid = uuid.uuid4()
log_output_file = "acc_balance.log"


def append_data_to_json(data_to_append: Dict[str, Any], file):

    log_client = LogsClient(output_file=log_output_file,
                            project_dir=project_dir,
                            file_name=file_name,
                            log_run_uuid=log_run_uuid)

    log_client.set_msg(log_type="info",
                       log_msg="beginning of function")

    try:

        log_client.set_msg(log_type="info",
                           log_msg="appending data to existing json file")

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

        log_client.set_msg(log_type="info",
                           log_msg="ending of function")

        return new_file_content

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def create_json(file_path: str, data_dict: Dict[str, Any]):

    log_client = LogsClient(output_file=log_output_file,
                            project_dir=project_dir,
                            file_name=file_name,
                            log_run_uuid=log_run_uuid)

    log_client.set_msg(log_type="info",
                       log_msg="beginning of function")

    try:

        log_client.set_msg(log_type="info",
                           log_msg="creating json file")

        with io.open(os.path.join(file_path), 'w') as f:

            f.write(json.dumps(data_dict))

        log_client.set_msg(log_type="info",
                           log_msg="ending of function")

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def _get_chrome_authenticated():

    log_client = LogsClient(output_file=log_output_file,
                            project_dir=project_dir,
                            file_name=file_name,
                            log_run_uuid=log_run_uuid)

    log_client.set_msg(log_type="info",
                       log_msg="beginning of function")

    try:

        bank_initial_page = BankWrapper(log_run_uuid=log_run_uuid,
                                        log_output_file=log_output_file,
                                        options=[])\
                                        .get_initial_page()

        log_client.set_msg(log_type="info",
                           log_msg="ending of function")

        return bank_initial_page

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def get_acc_balance():

    log_client = LogsClient(output_file=log_output_file,
                            project_dir=project_dir,
                            file_name=file_name,
                            log_run_uuid=log_run_uuid)

    log_client.set_msg(log_type="info",
                       log_msg="beginning of function")

    try:

        chrome = _get_chrome_authenticated()

        web_elem_xpath = '//*[@id="box_conteudo"]/table[1]/tbody/tr[1]/td[2]'

        log_client.set_msg(log_type="info",
                           log_msg=f"trying to reach element at xpath: {web_elem_xpath}")

        acc_elem = chrome.find_element_by_xpath(web_elem_xpath)

        log_client.set_msg(log_type="info",
                           log_msg="element was reached successfully")

        acc_balance_str = acc_elem.text.replace(".", "").replace(",", ".")[:-1]

        chrome.quit()

        log_client.set_msg(log_type="info",
                           log_msg="ending of function")

        return float(acc_balance_str)

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        chrome.quit()


def main():

    log_client = LogsClient(output_file=log_output_file,
                            project_dir=project_dir,
                            file_name=file_name,
                            log_run_uuid=log_run_uuid)

    log_client.set_msg(log_type="info",
                       log_msg="beginning of function")

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

        S3Bucket().upload_file(file_path=str(file_path))

        log_client.set_msg(log_type="info",
                           log_msg="ending of function")

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


if __name__ == "__main__":

    main()
