import sys
import threading
import subprocess

def run_script(case_no, viewpoint):
    script_name = f"../src/sim3D.py"
    #print(f"Starting {script_name}...")
    subprocess.run(["python3", script_name, str(case_no), viewpoint])
    #print(f"Finished {script_name}")

with open("../test/test_cases.txt", "r") as test_cases_file:
    lines = test_cases_file.readlines()[1:]  # Skip header line
    number_of_test_cases = len(lines)

    threads = []
    for viewpoint in ["diagonal", "sideon", "bowler", "top-down", "umpire", "batter", "wicket-keeper"]:  # produce one sim for each test case
        for idx, line in enumerate(lines):
            case_no = idx + 1  # case numbers start from 1
            #print(f"Running simulation for test case {case_no} of {number_of_test_cases} from {viewpoint}: {line.split(';')[-1].strip()}")
            t = threading.Thread(target=run_script, args=(case_no,viewpoint,))
            t.start()
            threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All scripts finished.")

sys.exit(0)



