import os
from multiprocessing import Pool


processes = ("acc_balance.py", "acc_expenses.py", "investments_balance.py")


def run_processes(process):
    os.system(f"python {process}") 


pool = Pool(processes=3)
pool.map(run_processes, processes)
