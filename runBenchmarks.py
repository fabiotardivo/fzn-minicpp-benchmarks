#!/usr/bin/env python3

import glob
import argparse
import subprocess
import os
import time
import argParser


# Argument parser
# ---
parser = argparse.ArgumentParser(description="Log the solving process of problems in MiniZinc format")
parser.add_argument("-b", help="Benchmark",   required=True,         )
parser.add_argument("-s", help="Solver",      required=True,         )
parser.add_argument("-t", help="Timeout [s]", required=True, type=int)

# Main
# ---

# Parse arguments
args = parser.parse_args()
benchmark, solver, timeout = argParser.getBenchmarkSolverTimeout(args)

# Select the MiniZinc model
mzn_filepath = "{}/{}".format(benchmark["path"], benchmark["model"])
if "gpu" in solver["tags"]:
    mzn_filepath = mzn_filepath.replace(".mzn", "_gpu.mzn")

# Create error and log files
log_filepath = "./{}_{}_{}_{}.log".format(benchmark["id"], solver["id"], timeout, time.strftime("%H%M-%d%m%Y"))
log_file = open(log_filepath, "w")
err_filepath = "./{}_{}_{}_{}.err".format(benchmark["id"], solver["id"], timeout, time.strftime("%H%M-%d%m%Y"))
err_file = open(err_filepath, "w")

# Collect the DataZinc files
dzn_filepath_list = sorted(glob.glob("{}/dzn/*.dzn".format(benchmark["path"])))
dzn_files_count = len(dzn_filepath_list)

# Solve each instance
for i in range(dzn_files_count):
    dzn_filepath = dzn_filepath_list[i]
    dzn_filename = os.path.split(dzn_filepath)[1]
    log_file.write("%%%mzn-stat: dzn={}\n".format(dzn_filename))
    log_file.flush()
    print("Solving {} using {} ({}/{}) ...".format(dzn_filepath, solver["id"], i + 1, dzn_files_count))
    cmd = ["minizinc", "--solver", solver["mzn_id"], "-s", "-a", "-t", str(timeout * 1000), "--output-time", mzn_filepath, dzn_filepath]
    subprocess.run(cmd, cwd="./", stdout=log_file, stderr=err_file)
    log_file.write("\n")
    log_file.flush()

# Close error and log files
log_file.close()
err_file.close()
