from wrapper_bank_initial_page import BankWrapper
from datetime import datetime
import json
from pathlib import Path
import io
import os
from typing import Dict, Any


def append_data_to_json(data_to_append: Dict[str, Any], file):

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
    return BankWrapper().get_initial_page()


def get_acc_balance():

    chrome = _get_chrome_authenticated()

    try:
        print("Getting cc balance...")
        acc_elem = chrome.find_element_by_xpath('//*[@id="box_conteudo"]/table[1]/tbody/tr[1]/td[2]')
        acc_balance_str = acc_elem.text.replace(".", "").replace(",", ".")[:-1]

        chrome.quit()

        return float(acc_balance_str)

    except Exception as e:
        print(f"Erro: {e.args}")
        chrome.quit()


def main():

    acc_balance_float = get_acc_balance()

    time_now = datetime.now()
    date_today = datetime.strftime(time_now, "%Y-%m-%d")

    dir_path = Path(__file__).resolve().parents[2]
    file_path = dir_path / Path(f"output_files/acc_balance_{date_today}.json")

    data_dict = {"time_check": str(time_now),
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


if __name__ == "__main__":
    main()
