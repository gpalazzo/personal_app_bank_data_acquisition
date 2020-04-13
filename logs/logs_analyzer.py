import glob
import pandas as pd
pd.set_option("display.max_columns", 10)
pd.set_option("display.max_rows", 20)

log_files = glob.glob("./logs_output/*")
df = pd.DataFrame(columns=["action_timestamp", "log_type", "file_name", "function_name", "run_uuid", "log_msg"])


for file in log_files:

    with open(file, "r") as f:

        for line in f:

            line_splitted = line.split(" - ")

            df_aux = pd.DataFrame(data={
                                        "action_timestamp": line_splitted[0],
                                        "log_type": line_splitted[1],
                                        "file_name": line_splitted[2],
                                        "function_name": line_splitted[3],
                                        "run_uuid": line_splitted[4],
                                        "log_msg": line_splitted[5].rstrip()
                                        },
                                  index=[0]
                                 )

            df = df.append(other=df_aux,
                           ignore_index=True)


print(df)