from src.wrappers.bank_webpage_auth import BankWrapper
from datetime import datetime
import json
from pathlib import Path
import io
import os
from typing import Dict, Any
from logs.logs_generator import LogsClient
import uuid
from selenium.webdriver import Chrome


project_dir = Path(__file__).resolve().parents[3]


log_client = LogsClient(output_file="bank_investments_balance.log",
                        project_dir=project_dir,
                        file_name=os.path.basename(__file__),
                        log_run_uuid=uuid.uuid4())


def append_data_to_json(data_to_append: Dict[str, Any], file):

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

        return new_file_content

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


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

        bank_initial_page = BankWrapper(log_run_uuid=log_client.log_run_uuid,
                                        log_output_file=log_client.output_file)\
                                        .get_initial_page()

        return bank_initial_page

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def get_rdc_lca_balance(chrome: Chrome):

    try:

        rdc_xpath = '//*[@id="box_conteudo"]/table[2]/tbody/tr[1]/td[2]/font'
        lca_xpath = '//*[@id="box_conteudo"]/table[2]/tbody/tr[2]/td[2]/font'
        log_client.set_msg(log_type="info",
                           log_msg=f"trying to reach elements at xpaths: {rdc_xpath} and {lca_xpath}")
        rdc = chrome.find_element_by_xpath(rdc_xpath)
        lca = chrome.find_element_by_xpath(lca_xpath)

        log_client.set_msg(log_type="info",
                           log_msg="elements were reached successfully")

        log_client.set_msg(log_type="info",
                           log_msg="parsing elements text properties")
        rdc_str = rdc.text.replace(".", "").replace(",", ".")
        lca_str = lca.text.replace(".", "").replace(",", ".")

        return rdc_str, lca_str

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        chrome.quit()


def main():

    try:

        log_client.set_msg(log_type="info",
                           log_msg="beginning of script")

        chrome = _get_chrome_authenticated()

        rdc, lca = get_rdc_lca_balance(chrome=chrome)

        time_now = datetime.now()
        date_today = datetime.strftime(time_now, "%Y-%m-%d")

        file_path = project_dir / Path(f"output_files/bank_investments_balance_{date_today}.json")

        data_dict = {"action_timestamp": str(time_now),
                     "rdc": rdc,
                     "lca": lca}

        if os.path.isfile(path=file_path) and os.access(file_path, os.R_OK):

            with open(file_path, 'r+') as f:

                file_content = append_data_to_json(data_dict, f)

                f.seek(0)

                f.truncate()

                json.dump(file_content, f)

        else:

            create_json(file_path=file_path, data_dict=data_dict)

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        log_client.set_msg(log_type="info",
                           log_msg="end of script")


if __name__ == "__main__":

    main()
