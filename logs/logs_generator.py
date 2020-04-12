import inspect
import logging
import traceback


class LogHandler:

    def __init__(self, project_dir: str, output_file: str):
        """Get both file name and function being executed only aiming ease the troubleshooting in case of errors.
        """
        self.output_log_file = output_file
        self.project_dir = project_dir
        self._set_log_config()

    def _set_log_config(self):
        logging.basicConfig(filename=f"{self.project_dir}/logs/logs_output/{self.output_log_file}.log",
                            level=logging.INFO,
                            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")


