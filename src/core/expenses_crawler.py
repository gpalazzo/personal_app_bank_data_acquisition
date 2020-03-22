from wrapper_bank_initial_page import BankWrapper
from time import sleep

# pd and re are only used in expenses crawler
import pandas as pd
import re

# get bank initial page after inserting env_var_handler
chrome = BankWrapper().get_initial_page()

# expenses crawler
try:
    print("Getting fatura cartão...")
    fatura_cartao = chrome.find_element_by_xpath('//*[@id="menu_rapido"]/div[1]/form/ul/li[9]/a')
    sleep(0.1)
    fatura_cartao.click()
    sleep(5)

    print("Hitting first buscar button...")
    js_function = "selecionar('consultarCartao')"
    chrome.execute_script(script=js_function)
    sleep(0.1)
    sleep(5)

    print("Hitting second buscar button...")
    js_function = "selecionar('consultarFatura')"
    chrome.execute_script(script=js_function)
    sleep(0.1)
    sleep(2)

    df = pd.DataFrame(columns={'Data', 'Empresa', 'Local', 'Valor'})

    print("Getting all expenses...")
    todos_gastos = chrome.find_elements_by_class_name('movimentosItem')

    for i, gasto in enumerate(todos_gastos):

        if i >= 5:
            splitted = gasto.text.split()
            data = splitted[0]
            valor = splitted[-1]
            split_2quotes = gasto.text.split("  ")

            for elem in split_2quotes:

                if data in elem:
                    empresa = re.sub(data, "", elem)
                    empresa = empresa.strip()

                if valor in elem:
                    local = re.sub(valor, "", elem)
                    local = local.strip()

            data_dict = {
                "Data": data,
                "Empresa": empresa,
                "Local": local,
                "Valor": valor
            }

            df = df.append(data_dict, ignore_index=True)

            if i == 10:
                break

    print(f"dataframe:\n{df}")

except Exception as e:
    print(f"Erro: {e.args}")
    chrome.quit()

chrome.quit()
