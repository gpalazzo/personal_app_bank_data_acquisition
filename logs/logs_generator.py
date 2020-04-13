import logging
import inspect
from uuid import uuid4


class LogsClient:

    def __init__(self,
                 output_file: str,
                 logs_dir: str,
                 file_name: str,
                 run_uuid: uuid4):
        """Get both file name and function being executed only aiming ease the troubleshooting in case of errors.
        """
        self.func_name = self._get_function_name()
        self.file_name = file_name
        self.run_uuid = run_uuid
        self._set_log_config(output_file=output_file,
                             logs_dir=logs_dir)

    @staticmethod
    def _set_log_config(output_file: str,
                        logs_dir: str):

        logging.basicConfig(filename=f"{logs_dir}/logs/logs_output/{output_file}",
                            level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _get_function_name():

        return inspect.stack()[2][3]

    def logging_begin(self):

        logging.info(msg=f"{self.file_name} - {self.func_name} - {self.run_uuid} - beginning of function")

    def logging_end(self):

        logging.info(msg=f"{self.file_name} - {self.func_name} - {self.run_uuid} - ending of function")

    def logging_set_msg(self, log_type: str = "", log_msg: str = ""):

        if log_type == "" or log_msg == "":

            raise ValueError("please provide log_type (e.g., info) and log_msg (e.g., running function)")

        else:

            if log_type == "info":

                logging.info(msg=f"{self.file_name} - {self.func_name} - {self.run_uuid} - {log_msg}")

            elif log_type == "error":

                logging.error(msg=f"{self.file_name} - {self.func_name} - {self.run_uuid} - {log_msg}")

            else:

                raise ValueError("please provide log_type as info or error")
