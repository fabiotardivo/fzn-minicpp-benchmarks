#!/usr/bin/env python3

import glob
import os
import pandas as pd

# Load known optimal solutions
solutions = pd.concat(pd.read_excel('Solutions.xlsx', sheet_name=None), ignore_index=True)

# Collect all BPP .txt files
files_paths = sorted(set(glob.glob("./BPP/*.bpp", recursive=True)))

for file_path in files_paths:
    file_name = os.path.basename(file_path)
    match = solutions.loc[solutions['Name'] == file_name, ["Best LB", "Best UB"]]

    if not match.empty:
        lb = match["Best LB"].iloc[0]
        ub = match["Best UB"].iloc[0]

        if lb == ub:
            # Read and parse BPP file
            with open(file_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                items = int(lines[0])
                capacity = int(lines[1])
                weights = [int(w) for w in lines[2:]]

            # Construct corresponding .dzn file path
            dzn_filepath = file_path.replace("BPP", "dzn").replace(".bpp", ".dzn")
            os.makedirs(os.path.dirname(dzn_filepath), exist_ok=True)

            # Write the .dzn file
            with open(dzn_filepath, "w") as dzn_file:
                dzn_file.write(f"items = {items};\n")
                dzn_file.write(f"capacity = {capacity};\n")
                dzn_file.write(f"n_bins = {lb};\n")
                dzn_file.write(f"weights = [{', '.join(map(str, weights))}];\n")

            print(f"[OK] {file_name} → {dzn_filepath}")
        else:
            print(f"[SKIP] {file_name} not optimally solved (LB ≠ UB)")
    else:
        print(f"[SKIP] {file_name} not found in Solutions.xlsx")
