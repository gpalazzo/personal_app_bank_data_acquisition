import os
from multiprocessing import Pool
from pathlib import Path

current_path = Path(__file__).resolve().parents[0]
processes = (f"{current_path}/acc_balance.py", f"{current_path}/acc_expenses.py", f"{current_path}/investments_balance.py")


def run_processes(process):
    os.system(f"python {process}") 


pool = Pool(processes=3)
pool.map(run_processes, processes)
