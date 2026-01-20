import os
import sys
import threading
import subprocess
import numpy as np
import shutil

### Delete all files
#shutil.rmtree("test_results")

### Run scripts
def run_gen_data_script(case_no):
    script_name = f"../src/plots3D.py"
    print(f"Starting {script_name}...")
    subprocess.run(["python3", script_name, str(case_no), str(0)])  # zero indicates no debug
    print(f"Finished {script_name} {case_no}")

with open("../test/test_cases.txt", "r") as test_cases_file:
    lines = test_cases_file.readlines()[1:]  # Skip header line
    number_of_test_cases = len(lines)

    threads = []
    for case_no, line in enumerate(lines):
        print(f"Running simulation for test case {case_no} of {number_of_test_cases}: {line.split(';')[-1].strip()}")
        t = threading.Thread(target=run_gen_data_script, args=(case_no,))
        t.start()
        threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All data generator scripts finished.")

### Do collation plots for comparisons in range
def run_collate_plots_script(name, values):
    script_name = "collate_plots.py"
    print(f"Starting {script_name} for {name}...")
    # join values into a single string argument (e.g. "val1,val2,...")
    values_str = ",".join(values)
    subprocess.run(["python3", script_name, str(name), values_str])
    print(f"Finished {script_name} {name}")

test_results_dir = "../test/test_results"
directory_names = [d for d in os.listdir(test_results_dir) if os.path.isdir(os.path.join(test_results_dir, d))]

# Split potential values from test names
def number_in(word):
    for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if str(n) in word:
            return True
    return False

directory_names_tuples = []
for d in directory_names:
    if number_in(d):
        parts = d.split("_")
        tuple_entry = ["_".join(parts[:-1]), parts[-1]]
        directory_names_tuples.append(tuple_entry)

# Find matching test names
matching_tests = {}
unique_prefixes = np.unique([t[0] for t in directory_names_tuples])
threads = []
for prefix in unique_prefixes:
    # For each test name which has matching ones, get the values (t[1] where t[0] == prefix)
    values = [t[1] for t in directory_names_tuples if t[0] == prefix]
    matching_tests[prefix] = values

    t = threading.Thread(target=run_collate_plots_script, args=(prefix, values,))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All collation plots finished.")

sys.exit(0)

'''
import sys
from multiprocessing import Pool
import subprocess
import numpy as np
import os

def run_script(case_no):
    script_path = "../src/trial.py"
    print(f"Starting {script_path} {case_no}...")
    subprocess.run(["python3", script_path, str(case_no)])
    print(f"Finished {script_path} {case_no}")

if __name__ == "__main__":
    with open("../test/test_cases.txt", "r") as test_cases_file:
        lines = test_cases_file.readlines()[1:]  # Skip header line
    number_of_test_cases = len(lines)
    case_numbers = np.arange(0, number_of_test_cases)
    with Pool() as pool:
        pool.map(run_script, case_numbers)


sys.exit(0)
'''



