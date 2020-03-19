from typing import Dict, List, Any
import psycopg2
from bank_microservice.hidden_info.hidden_info_loader import PersonalInfoLoader
from bank_microservice.src.aux.sql_queries import SQLQueries
from logs_microservice.logs import LogHandler


class DBClient:
    """Class to connect to the database and define db methods'.
    """

    def __init__(self, db_name: str):
        """Creates connection and cursor to the database.
        Args:
            db_name: database name
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.config = PersonalInfoLoader().load_config
        self.credentials = PersonalInfoLoader().load_credentials
        self.cnn = psycopg2.connect(user=self.credentials["aws"]["rds"]["master_username"],
                                    password=self.credentials["aws"]["rds"]["master_password"],
                                    database=db_name,
                                    host=self.config["aws"]["rds"]["endpoint"],
                                    port=self.config["aws"]["rds"]["port"])

        self.cursor = self.cnn.cursor()

    def _execute_sql_statement(self, sql_query: str):
        """Execute and commit statements to the database. Statement is usually represented by a SQL query as string.
        Args:
            str_query: SQL query as string to be executed
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        self.cursor.execute(sql_query)
        self.cnn.commit()

    def insert_new_record(self, tbl_name: str, values: Dict[str, Any]):
        """Insert new record into a table using INSERT INTO SQL clause.
        Args:
            tbl_name: table name
            values: values to be inserted in the table. The dictionary key's must represent table column's name
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        # cols = self._get_cols_names(tbl_name=tbl_name)
        sql_query = SQLQueries.insert_into(tbl_name=tbl_name, values=values)
        self._execute_sql_statement(sql_query=sql_query)
        self.cnn.close()

    def _get_cols_names(self, tbl_name: str) -> List:
        """Get the name of the columns of a given table.
        Args:
            tbl_name: table name
        Returns:
            name of the columns
        """

        log_handler = LogHandler()
        func_name, file_name = log_handler.func_name, log_handler.file_name

        print(f"Executing function: {func_name} in file: {file_name}")

        sql_query = SQLQueries.get_table_info(tbl_name=tbl_name)
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()

        cols = []

        for _tuple in result:
            cols.append(_tuple[0])

        return cols
