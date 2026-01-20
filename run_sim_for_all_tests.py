import sys
import threading
import subprocess

def run_script(case_no):
    script_name = f"trial.py" + " "  + str(case_no)
    print(f"Starting {script_name}...")
    subprocess.run(["python3", script_name])
    print(f"Finished {script_name}")

with open("../test/test_cases.txt", "r") as test_cases_file:
    lines = test_cases_file.readlines()[1:]  # Skip header line
    number_of_test_cases = len(lines)

    threads = []
    for case_no, line in enumerate(lines):
        print(f"Running simulation for test case {case_no} of {number_of_test_cases}: {line.split(';')[-1].strip()}")
        t = threading.Thread(target=run_script, args=(case_no,))
        t.start()
        threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All scripts finished.")

sys.exit(0)

'''
import sys
from multiprocessing import Pool
import subprocess
import numpy as np

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



