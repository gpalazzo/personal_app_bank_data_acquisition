from wrapper_bank_initial_page import BankWrapper
from datetime import datetime
import json
from pathlib import Path
import io
import os


dir_path = Path(__file__).resolve().parents[2]
chrome = BankWrapper().get_initial_page()

try:
    print("Getting cc balance...")
    acc_elem = chrome.find_element_by_xpath('//*[@id="box_conteudo"]/table[1]/tbody/tr[1]/td[2]')
    acc_balance_str = acc_elem.text.replace(".", "").replace(",", ".")[:-1]

    chrome.quit()

    acc_balance_float = float(acc_balance_str)

    data_dict = {"time_check": str(datetime.now()),
                 "acc_balance": acc_balance_float,
                 "email_status": "not_sent"}

    with io.open(os.path.join(dir_path, 'output_files/acc_balance.json'), 'w') as f:
        f.write(json.dumps(data_dict))

except Exception as e:
    print(f"Erro: {e.args}")
    chrome.quit()
