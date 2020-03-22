import psycopg2
from bank_microservice.env_var_handler import PersonalInfoLoader

config = PersonalInfoLoader().load_config
credentials = PersonalInfoLoader().load_credentials
cnn = psycopg2.connect(user=credentials["aws"]["rds"]["master_username"],
                        password=credentials["aws"]["rds"]["master_password"],
                        database="financial",
                        host=config["aws"]["rds"]["endpoint"],
                        port=config["aws"]["rds"]["port"])
cursor = cnn.cursor()

# print(f"cnn: {cnn}")
# print(f"cursor: {cursor}")

sql_query = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'account_balance';
            """

# sql_query = "SELECT * FROM account_balance"
#
cursor.execute(sql_query)
# # #
print(f"result: {cursor.fetchall()}")
# #
cnn.close()