#!/usr/bin/env python3

import sys
import argparse
import csv
import glob
import re
import logParser
import argParser

def getLogFile(benchmark, solver, timeout):
    log_files = glob.glob("./{}_{}_{}_*.log".format(benchmark, solver,timeout))
    if len(log_files) == 0:
        sys.exit("File {}_{}_{}_*.log not found".format(benchmark,solver,timeout))
    elif len(log_files) > 1:
        sys.exit("Too many files of the forms {}_{}_{}_*.log".format(benchmark, solver,timeout))
    else:
        return log_files[0]

def normalizeLog(log_content):
    log_content = re.sub(r"^\s*\n",                              "", log_content, flags=re.MULTILINE) # Remove blank lines
    log_content = re.sub(r"% Generated FlatZinc statistics:\n",  "", log_content, flags=re.MULTILINE) # Remove FlatZinc comments
    log_content = re.sub(r"%%%mzn-stat: .*=\".*\"\n",            "", log_content, flags=re.MULTILINE) # Remove not numeric statistics
    log_content = re.sub(r"%%%mzn-stat: time=.*\n",              "", log_content, flags=re.MULTILINE) # Remove time
    log_content = re.sub(r"%% =====TIME-OUT=====\n",             "", log_content, flags=re.MULTILINE) # Remove timeout comment (Jacop)
    return log_content


# Argument parser
# ---
parser = argparse.ArgumentParser(description="Converts MiniZin logs files to CSV files.")
parser.add_argument("-b", help="Benchmark",         required=True,         )
parser.add_argument("-s", help="Solver",            required=True,         )
parser.add_argument("-t", help="Timeout [s]",       required=True, type=int)

# Main
# ---
# Parse arguments
args = parser.parse_args()
benchmark, solver, timeout = argParser.getBenchmarkSolverTimeout(args)

# Read log file
log_filepath = getLogFile(benchmark["id"], solver["id"], timeout)
log_file = open(log_filepath, "r")
log_content = log_file.read()
log_file.close()
log_content = normalizeLog(log_content)
#print(log_content)

# Parse log file
log_tree = logParser.FznOutputGrammar.parse(log_content)
log_data = logParser.FznOutputVisitor().visit(log_tree)

# Write statistics CSV
csv_filepath = log_filepath.replace(".log","_stats.csv")
csv_file = open(csv_filepath, "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(log_data["stats_header"])
csv_writer.writerows(log_data["stats_rows"])
csv_file.close()

# Write results CSV
csv_filepath = log_filepath.replace(".log","_results.csv")
csv_file = open(csv_filepath, "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(log_data["results_header"])
csv_writer.writerows(log_data["results_rows"])
csv_file.close()
