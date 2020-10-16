import logging
import inspect
from uuid import uuid4
from utils.config_vars import LOGS_FILES_OUTPUT_DIR


class LogsClient:

    def __init__(self,
                 output_file: str,
                 project_dir: str,
                 file_name: str,
                 log_run_uuid: uuid4):
        """Get both file name and function being executed only aiming ease the troubleshooting in case of errors.
        """
        self.file_name = file_name
        self.log_run_uuid = log_run_uuid
        self.output_file = output_file
        self._set_log_config(output_file=self.output_file,
                             project_dir=project_dir)

    @staticmethod
    def _set_log_config(output_file: str,
                        project_dir: str):

        logging.basicConfig(filename=f"{project_dir}/{LOGS_FILES_OUTPUT_DIR}/{output_file}",
                            level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_caller_func_name():

        return inspect.stack()[2][3]

    def set_msg(self, log_type: str = "", log_msg: str = ""):

        func_name = self._get_caller_func_name()

        if log_type == "" or log_msg == "":

            raise ValueError("please provide log_type (e.g., info) and log_msg (e.g., running function)")

        else:

            if log_type == "info":

                logging.info(msg=f"{self.file_name} - {func_name} - {log_msg} - {self.log_run_uuid}")

            elif log_type == "error":

                logging.error(msg=f"{self.file_name} - {func_name} - {log_msg} - {self.log_run_uuid}")

            else:

                raise ValueError("please provide log_type as info or error")
