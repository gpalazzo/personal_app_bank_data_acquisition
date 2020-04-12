from wrapper_bank_initial_page import BankWrapper
from datetime import datetime
import json
from pathlib import Path
import io
import os
from typing import Dict, Any
from src.clients.aws_s3_bucket import S3Bucket
from logs.logs_generator import LogHandler
import logging


project_dir = Path(__file__).resolve().parents[2]


def append_data_to_json(data_to_append: Dict[str, Any], file):

    # log_obj = LogHandler(project_dir=project_dir,
    #                      output_file="acc_balance")
    #
    # logging.info(log_obj.func_exec_name)
    # logging.info(log_obj.file_exec_name)

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


def create_json(file_path: str, data_dict: Dict[str, Any]):

    with io.open(os.path.join(file_path), 'w') as f:
        f.write(json.dumps(data_dict))


def _get_chrome_authenticated():

    # log_obj = LogHandler(project_dir=project_dir,
    #                      output_file="acc_balance")
    #
    # logging.info(log_obj.func_exec_name)
    # logging.info(log_obj.file_exec_name)

    return BankWrapper().get_initial_page()


def get_rdc_lca_balance():

    # log_obj = LogHandler(project_dir=project_dir,
    #                      output_file="acc_balance")
    #
    # logging.info(log_obj.func_exec_name)
    # logging.info(log_obj.file_exec_name)

    chrome = _get_chrome_authenticated()

    try:
        print("Getting cc balance...")
        rdc = chrome.find_element_by_xpath('//*[@id="box_conteudo"]/table[2]/tbody/tr[1]/td[2]/font')
        lca = chrome.find_element_by_xpath('//*[@id="box_conteudo"]/table[2]/tbody/tr[2]/td[2]/font')

        rdc_str = rdc.text.replace(".", "").replace(",", ".")[:-1]
        lca_str = lca.text.replace(".", "").replace(",", ".")[:-1]

        chrome.quit()

        return float(rdc_str), float(lca_str)

    except Exception as e:
        print(f"Erro: {e.args}")
        chrome.quit()


def main():

    log_obj = LogHandler(project_dir=project_dir,
                         output_file="acc_balance")

    logging.info(log_obj.func_exec_name)
    logging.info(log_obj.file_exec_name)

    rdc, lca = get_rdc_lca_balance()

    time_now = datetime.now()
    date_today = datetime.strftime(time_now, "%Y-%m-%d")

    dir_path = Path(__file__).resolve().parents[2]
    file_path = dir_path / Path(f"output_files/investments_balance_{date_today}.json")

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

    S3Bucket().upload_file(file_path=str(file_path))


if __name__ == "__main__":
    main()
