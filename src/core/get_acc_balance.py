from wrapper_bank_initial_page import BankWrapper
from datetime import datetime
import json


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

    json_dump_str = json.dumps(obj=data_dict)
    json_loaded = json.loads(s=json_dump_str)

    with open("output_files/acc_balance.json", "w") as f:
        json.dump(obj=json_loaded, fp=f)

except Exception as e:
    print(f"Erro: {e.args}")
    chrome.quit()
