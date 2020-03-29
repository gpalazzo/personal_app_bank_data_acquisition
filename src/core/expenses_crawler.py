from wrapper_bank_initial_page import BankWrapper
from time import sleep
import json
import pandas as pd
import re
import os
import io
from datetime import datetime
from pathlib import Path


def _parse_dataframe(df: pd.DataFrame):

    try:

        return df.to_json(orient="index")

    except Exception as e:

        print(f"Error args: {e.args}")


def create_json(file_path: str, json_content):

    try:

        with io.open(os.path.join(file_path), 'w') as f:
            f.write(json.dumps(json_content))

    except Exception as e:
        print(f"Error args: {e.args}")


def _get_chrome_authenticated():

    return BankWrapper().get_initial_page()


def get_expenses() -> pd.DataFrame:

    chrome = _get_chrome_authenticated()

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

        df = pd.DataFrame(columns={"date", "company", "place", "value", "action_timestamp"})

        print("Getting all expenses...")
        all_expenses = chrome.find_elements_by_class_name('movimentosItem')

        initial_tr_number = 9999

        for i, expense in enumerate(all_expenses, 1):

            # if True, it means it's reading the TOTAL which I don't want to save here
            if i == len(all_expenses):
                break

            else:

                if "GASTOS DE GUILHERME PALAZZO" in expense.text:
                    initial_tr_number = i

                else:

                    if i > initial_tr_number:

                        time_now = str(datetime.now())

                        splitted = expense.text.split()
                        date = splitted[0]
                        value = splitted[-1]
                        split_2quotes = expense.text.split("  ")

                        for elem in split_2quotes:

                            if date in elem:
                                company = re.sub(date, "", elem)
                                company = company.strip()

                            if value in elem:
                                place = re.sub(value, "", elem)
                                place = place.strip()

                        data_dict = {
                            "date": date,
                            "company": company,
                            "place": place,
                            "value": value,
                            "action_timestamp": time_now
                        }

                        # even though I'm going to generate JSON again, working with data frames simplify the process
                        df = df.append(data_dict, ignore_index=True)

                    else:
                        continue

        return df

    except Exception as e:
        print(f"Erro: {e.args}")
        chrome.quit()

    chrome.quit()


def main():

    expenses = get_expenses()

    json_content_str = _parse_dataframe(expenses)

    json_content = json.loads(json_content_str)

    date_today = datetime.strftime(datetime.now(), "%Y-%m-%d")

    dir_path = Path(__file__).resolve().parents[2]
    file_path = dir_path / Path(f"output_files/acc_expenses_{date_today}.json")

    create_json(file_path=file_path, json_content=json_content)


if __name__ == "__main__":
    main()
