from typing import Dict, Any
from logs_microservice.logs import LogHandler


class SQLQueries:
    """Class to store all SQL queries.
    """

    def get_table_info(tbl_name: str) -> str:
        """Query to retrieve structural info from the table, e.g., column names
            Args:
                tbl_name: table name
            Returns:
                SQL query as string
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        return f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{tbl_name}'
                """

    def insert_into(tbl_name: str, values: Dict[str, Any]) -> str:
        """Query to insert values into a table.
            Args:
                tbl_name: table name
                cols: name of the columns
                values: dict of the values to be inserted
            Returns:
                SQL query as string
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        return f"""INSERT INTO {tbl_name}
                   VALUES ('{values["date_balance"]}', {values["value_balance"]}, '{values["email_status"]}')"""

    def get_next_id(tbl_name) -> str:
        """Query to get next id value.
            Args:
                tbl_name: table name
            Returns:
                SQL query as string
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        return f"""SELECT MAX(id) + 1 FROM {tbl_name}"""
