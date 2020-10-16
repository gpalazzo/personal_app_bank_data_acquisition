from src.wrappers.bank_webpage_auth import BankWrapper
from time import sleep
import json
import pandas as pd
import re
import os
import io
from datetime import datetime
from pathlib import Path
from logs.logs_generator import LogsClient
import uuid
from selenium.webdriver import Chrome
from utils.config_vars import *


local_project_root_dir = Path(__file__).resolve().parents[5]


log_client = LogsClient(output_file="bank_acc_expenses.log",
                        project_dir=local_project_root_dir,
                        file_name=os.path.basename(__file__),
                        log_run_uuid=uuid.uuid4())


def _parse_dataframe(df: pd.DataFrame):

    try:

        log_client.set_msg(log_type="info",
                           log_msg="parsing dataframe")

        df_parsed = df.to_json(orient="index")

        return df_parsed

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def create_json(file_path: str, json_content):

    try:

        log_client.set_msg(log_type="info",
                           log_msg="creating json")

        with io.open(os.path.join(file_path), 'w') as f:
            f.write(json.dumps(json_content))

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


def get_expenses(chrome: Chrome) -> pd.DataFrame:

    try:

        xpath = '//*[@id="menu_rapido"]/div[1]/form/ul/li[9]/a'
        log_client.set_msg(log_type="info",
                           log_msg=f"reaching `fatura cartão` at xpath: {xpath}")
        fatura_cartao = chrome.find_element_by_xpath(xpath)
        sleep(0.1)
        log_client.set_msg(log_type="info",
                           log_msg=f"clicking `fatura cartão` at xpath: {xpath}")
        fatura_cartao.click()
        sleep(5)

        js_function = "selecionar('consultarCartao')"
        log_client.set_msg(log_type="info",
                           log_msg=f"executing `first buscar button` through js function: {js_function}")
        chrome.execute_script(script=js_function)
        sleep(0.1)
        sleep(5)

        js_function = "selecionar('consultarFatura')"
        log_client.set_msg(log_type="info",
                           log_msg=f"executing `second buscar button` through js function: {js_function}")
        chrome.execute_script(script=js_function)
        sleep(0.1)
        sleep(2)

        df = pd.DataFrame(columns={"date", "company", "place", "value", "action_timestamp"})

        class_name = "movimentosItem"
        log_client.set_msg(log_type="info",
                           log_msg=f"reaching `expense itens` at class name: {class_name}")
        all_expenses = chrome.find_elements_by_class_name(class_name)

        initial_tr_number = 9999

        log_client.set_msg(log_type="info",
                           log_msg="looping over all expenses")
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

                        log_client.set_msg(log_type="info",
                                           log_msg="parsing elements text properties")

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

                        log_client.set_msg(log_type="info",
                                           log_msg="creating dict with parsed elements")

                        data_dict = {
                            "date": date,
                            "company": company,
                            "place": place,
                            "value": value,
                            "action_timestamp": time_now
                        }

                        log_client.set_msg(log_type="info",
                                           log_msg="appending dataframe")
                        # even though I'm going to generate JSON again, working with data frames simplify the process
                        df = df.append(data_dict, ignore_index=True)

                    else:

                        continue

        return df

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

        expenses = get_expenses(chrome=chrome)

        json_content_str = _parse_dataframe(expenses)

        json_content = json.loads(json_content_str)

        date_today = datetime.strftime(datetime.now(), "%Y-%m-%d")

        file_path = local_project_root_dir / Path(f"{FINANCIAL_DATA_FILES_OUTPUT_DIR}/bank_acc_expenses_{date_today}.json")

        create_json(file_path=file_path, json_content=json_content)

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        log_client.set_msg(log_type="info",
                           log_msg="end of script")


if __name__ == "__main__":

    main()
