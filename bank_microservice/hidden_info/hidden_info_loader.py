import yaml
from pathlib import Path
from typing import Dict
from logs_microservice.logs import LogHandler


def _get_hidden_info_local_path() -> Dict[str, str]:
    """Get local path from yml file.
    Returns:
        dict containing relative path to local info storage
    """

    log_handler = LogHandler()
    func_name, file_name = log_handler.func_name, log_handler.file_name

    print(f"Executing function: {func_name} in file: {file_name}")

    project_dir = str(Path(__file__).resolve().parents[0])
    with open(f"{project_dir}/hidden_info_local_path.yml", "r") as f:
        return yaml.safe_load(f)


hidden_info_path = _get_hidden_info_local_path()
local_path = str(Path(__file__).resolve().parents[3]) + hidden_info_path["hidden_info"]["local_path"]


class PersonalInfoLoader:
    """Class for loading personal info stored locally.
    """

    def __init__(self):
        """Creates instance of the class and loads all personal info.
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.load_credentials = self._credentials_loader()
        self.load_config = self._config_loader()

    @staticmethod
    def _credentials_loader() -> Dict[str, str]:
        """Load credentials.
        Returns:
            dict containing personal credentials info
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        with open(f"{local_path}/personal_info/credentials.yml", "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def _config_loader() -> Dict[str, str]:
        """Load configs.
        Returns:
            dict containing personal config info
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        with open(f"{local_path}/personal_info/config.yml", "r") as f:
            return yaml.safe_load(f)


class ThirdPartyInfoLoader:
    """Class for loading third party info stored locally.
    """

    def __init__(self):
        """Creates instance of the class and loads all third party info.
        """
        self.load_emails = self._emails_loader()

    @staticmethod
    def _emails_loader() -> Dict[str, str]:
        """Load emails.
        Returns:
            dict containing third party emails
        """
        with open(f"{local_path}/third_party_info/emails.yml", "r") as f:
            return yaml.safe_load(f)
