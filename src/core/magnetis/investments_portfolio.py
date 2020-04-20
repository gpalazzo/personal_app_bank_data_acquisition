from src.wrappers.magnetis_webpage_auth import MagnetisWrapper
from datetime import datetime
from src.clients.aws_s3_bucket import S3Bucket
from logs.logs_generator import LogsClient
from pathlib import Path
import uuid
from typing import Dict, Any
import json
import io
import os
from selenium.webdriver import Chrome
from time import sleep


project_dir = Path(__file__).resolve().parents[3]


log_client = LogsClient(output_file="magnetis_investments_portfolio.log",
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
                       log_msg="getting chrome authenticated through magnetis wrapper")

    try:

        magnetis_initial_page = MagnetisWrapper(log_run_uuid=log_client.log_run_uuid,
                                                log_output_file=log_client.output_file,
                                                options=[])\
                                                .get_initial_page()

        return magnetis_initial_page

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")


def get_investments_portfolio(chrome: Chrome):

    try:

        xpath = '//*[@id="root"]/div/main/div[4]/a/i'

        log_client.set_msg(log_type="info",
                           log_msg=f"trying to reach element at xpath: {xpath}")

        portfolio_drill_down = chrome.find_element_by_xpath(xpath=xpath)
        sleep(2)

        log_client.set_msg(log_type="info",
                           log_msg="element was reached successfully")

        log_client.set_msg(log_type="info",
                           log_msg=f"action click on elem: {portfolio_drill_down}")

        portfolio_drill_down.click()

        sleep(5)

        class_name = "category_1rId8"
        log_client.set_msg(log_type="info",
                           log_msg=f"trying to reach element with class name: {class_name}")

        assets_distribution = chrome.find_elements_by_class_name(name=class_name)
        sleep(2)

        log_client.set_msg(log_type="info",
                           log_msg="element was reached successfully")

        assets = {}

        for asset_settings in assets_distribution:

            # [0]: asset_name, [1]: asset current balance, [2]: asset return pct, [3]: asset pct portfolio
            asset_settings_list = asset_settings.text.split("\n")
            assets[asset_settings_list[0]] = {"balance": asset_settings_list[1],
                                              "return_pct": asset_settings_list[2],
                                              "portfolio_pct": asset_settings_list[3]}

        return assets

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        chrome.quit()


def main():

    log_client.set_msg(log_type="info",
                       log_msg="beginning of script")

    try:

        chrome = _get_chrome_authenticated()

        data_dict = get_investments_portfolio(chrome=chrome)

        time_now = datetime.now()

        date_today = datetime.strftime(time_now, "%Y-%m-%d")

        file_path = project_dir / Path(f"output_files/magnetis_investments_portfolio_{date_today}.json")

        data_dict.update({"action_timestamp": str(time_now)})

        if os.path.isfile(path=file_path) and os.access(file_path, os.R_OK):

            with open(file_path, 'r+') as f:

                file_content = append_data_to_json(data_dict, f)

                f.seek(0)

                f.truncate()

                json.dump(file_content, f)

        else:

            create_json(file_path=file_path, data_dict=data_dict)

        S3Bucket().upload_file(file_path=str(file_path))

    except Exception as e:

        log_client.set_msg(log_type="error",
                           log_msg=f"the following error occurred with args: {e.args}")

    finally:

        log_client.set_msg(log_type="info",
                           log_msg="end of script")


if __name__ == "__main__":

    main()
