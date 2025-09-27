#!/usr/bin/env python3

import pandas as pd
import subprocess

dzn_dir   = "dzn"
fzn_dir   = "fzn-sat"
solver_id = "org.minicpp.ml"
model_filename = "rcpsp-sat.mzn"
silution_filename = "solutions.csv"

solutions = pd.read_csv(silution_filename)
for _, row  in solutions.iterrows():
    dzn_filename, lb, ub = row
    dzn_filepath = f"{dzn_dir}/{dzn_filename}"
    print(f"Converting {dzn_filepath} ", end="")
    if (lb == ub):
        fzn_filename = dzn_filename.replace(".dzn", ".fzn")
        fzn_filepath = f"{fzn_dir}/{fzn_filename}"
        result = subprocess.run([
            "minizinc",
            "--solver", solver_id,
            "--compile", "--no-output-ozn",
            model_filename,
            dzn_filepath, "-D", f"makespan={ub}",
            "-o", fzn_filepath])
        print("[OK]" if result.returncode == 0 else "[FAILED]")
    else:
        print("[SKIPPED]")
