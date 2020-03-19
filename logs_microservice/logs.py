import inspect


class LogHandler:

    def __init__(self):
        """Get both file name and function being executed only aiming ease the troubleshooting in case of errors.
        """
        context = inspect.stack()
        call_origin = str(context[1])
        call_origin_splitted = call_origin.split(",")
        self.func_name = self._get_function_name(call_origin_splitted)
        self.file_name = self._get_file_name(call_origin_splitted)

    @staticmethod
    def _get_function_name(_list):

        for elem in _list:
            if "function=" in elem:
                func_name = elem.split("=")
                return func_name[1]
            else:
                continue

    @staticmethod
    def _get_file_name(_list):

        for elem in _list:
            if "filename=" in elem:
                file_name = elem.split("=")
                return file_name[1]
            else:
                continue
