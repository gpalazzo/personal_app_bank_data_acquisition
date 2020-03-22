from wrapper_bank_initial_page import BankWrapper

chrome = BankWrapper().get_initial_page()

try:
    print("Getting cc balance...")
    cc_elem = chrome.find_element_by_xpath('//*[@id="box_conteudo"]/table[1]/tbody/tr[1]/td[2]')
    cc_balance_str = cc_elem.text.replace(".", "").replace(",", ".")[:-1]
    print(f"saldo conta: {cc_balance_str}")
    assert False, "break proposital."
    db_client = DBClient(db_name="financial")
    print("Updating database...")
    db_client.insert_new_record(tbl_name="account_balance",
                                values={"date_balance": date.today(),
                                        "value_balance": float(cc_balance_str),
                                        "email_status": "email_sent"})

except Exception as e:
    print(f"Erro: {e.args}")
    chrome.quit()

chrome.quit()
