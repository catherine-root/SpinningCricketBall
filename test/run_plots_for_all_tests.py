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
    #print(f"Starting {script_name}...")
    subprocess.run(["python3", script_name, str(case_no), str(0)])  # zero indicates no debug
    #print(f"Finished {script_name} {case_no}")

with open("../test/test_cases.txt", "r") as test_cases_file:
    lines = test_cases_file.readlines()[1:]  # Skip header line
    number_of_test_cases = len(lines)

    threads = []
    for idx, line in enumerate(lines):
        case_no = idx + 1  # case numbers start from 1
        #print(f"Running simulation for test case {case_no} of {number_of_test_cases}: {line.split(';')[-1].strip()}")
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
    #print(f"Starting {script_name} for {name}...")
    # join values into a single string argument (e.g. "val1,val2,...")
    values_str = ",".join(values)
    subprocess.run(["python3", script_name, str(name), values_str])
    #print(f"Finished {script_name} {name}")

test_results_dir = "../test/test_results"
global directory_names
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



# Summary file for batch of test cases
directory_names = [d for d in os.listdir(test_results_dir) if os.path.isdir(os.path.join(test_results_dir, d))]

def find_and_write_exit_status(write_file):

    exits = {}
    count = 0
    for name in directory_names:
        directory_test_case_results = f"test_results/{name}"
        full_file_path = directory_test_case_results+"/plot3D_exit_status.txt"
        if os.path.exists(full_file_path):  # catch collate_plot created directories
            with open(full_file_path, "r") as f:
                file_contents = f.readlines()
                exit_status = file_contents[-1].strip()  # last line is exit status
                if exit_status not in exits:
                    exits[exit_status] = 1
                else:
                    exits[exit_status] += 1
            count += 1

    with open(write_file, "a") as f:
        f.write(f"\nExit status summary for {count} test cases:\n\n")
        for exit_status in exits.keys():
            f.write(f"{exit_status}\n{exits[exit_status]}\n\n")

def get_extrema():
    extrema_dict = {}
    #print(directory_names)
    #print(directory_names_tuples)

    first_pass = True

    for name in directory_names:
        directory_test_case_results = f"test_results/{name}"

        if first_pass:  # populate extrema
            for filename in ["plot3D_output.txt", "plot3D_forces.txt"]:
                full_file_path = directory_test_case_results+"/"+filename
                if os.path.exists(full_file_path):  # catch collate_plot created directories
                    with open(full_file_path, "r") as f:
                        file_contents = f.readlines()
                        header = file_contents[0].strip().split(',') 
                        lines = file_contents[1:]  # Skip header
                        data_matrix = np.zeros((len(lines), 9))  # t,x,y,z,vx,vy,vz,horizontal_angle,elevation_angle
                        for i, line in enumerate(lines):
                            data_matrix[i] = np.array(line.strip().split(','), dtype=float)
                    
                        # read first line of output file and forces file to get index of column to extract for each parameter
                        for idx, parameter in enumerate(header):
                            if len(data_matrix[:,idx]) > 0:  # catch empty files
                                extrema_dict[parameter] = [min(data_matrix[:,idx]), max(data_matrix[:,idx])]
                        first_pass = False


        else:  # update extrema as required
            for filename in ["plot3D_output.txt", "plot3D_forces.txt"]:
                full_file_path = directory_test_case_results+"/"+filename
                if os.path.exists(full_file_path):  # catch collate_plot created directories
                    with open(full_file_path, "r") as f:
                        file_contents = f.readlines()
                        header = file_contents[0].strip().split(',') 
                        lines = file_contents[1:]  # Skip header
                        data_matrix = np.zeros((len(lines), 9))  # t,x,y,z,vx,vy,vz,horizontal_angle,elevation_angle
                        for i, line in enumerate(lines):
                            data_matrix[i] = np.array(line.strip().split(','), dtype=float)

                        # read first line of output file and forces file to get index of column to extract for each parameter
                        for idx, parameter in enumerate(header):
                            if len(data_matrix[:,idx]) > 0:  # catch empty files
                                if min(data_matrix[:,idx]) < extrema_dict[parameter][0]:
                                    extrema_dict[parameter] = [min(data_matrix[:,idx]), extrema_dict[parameter][1]]
                                if max(data_matrix[:,idx]) > extrema_dict[parameter][1]:
                                    extrema_dict[parameter] = [extrema_dict[parameter][0], max(data_matrix[:,idx])]

    return extrema_dict

def pad_string(s, desired_length, where="end"):
    alt = 1
    while len(s) < desired_length:
        if where == "end":
            s += " "
        else:  # where == "both"
            if alt == 1:
                s = " " + s
            else:  # alt = -1
                s = s + " "
            alt *= -1
    return s

def write_extrema(write_file, extrema):
    with open(write_file, "a") as f:
        f.write("\nText which won't appear in the summary output file ------------------------- \n")
        f.write("\nParameter  |   Minimum  |  Maximum\n")
        f.write("-------------------------------------\n")
        for p in extrema.keys():
            f.write(f"{pad_string(p, len('horizontal_angle')+1, 'end')}|{pad_string(str(extrema[p][0]), 10, 'both')}|{pad_string(str(extrema[p][1]), 10, 'both')}\n")
        f.write("\n\n\n")


import datetime
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
summary_filename = "plot3D_summary"+timestamp+".txt"
if os.path.exists("test_results/"+summary_filename):
    os.remove("test_results/"+summary_filename)
with open("test_results/"+summary_filename, "w") as f:
    f.write(f"Summary of batch of test results from: {timestamp}\n\n")

    # read all test cases

    # write default parameters for this batch = test case 1 (or 0) parameters

    # maximums and minimums for some parameters: x, y, z, vx, vy, vz, ax, ay, az, angles, etc
    extrema_dictionary = get_extrema()
    write_extrema("test_results/"+summary_filename, extrema_dictionary)

    # find out which ones did of did not bounce
    # which ones went too far to the side of the pitch
    find_and_write_exit_status("test_results/"+summary_filename)

print("Summary file created.")




sys.exit(0)