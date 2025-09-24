
import os
import pandas as pd

def load_optimal_instances(solution_file):
    df = pd.read_excel(solution_file)
    df["Best UB"] = df["Best UB"].round().astype("Int64")
    df["Best LB"] = df["Best LB"].round().astype("Int64")
    df_optimal = df[df["Best UB"] == df["Best LB"]]
    return dict(zip(df_optimal["Instance"], df_optimal["Best LB"]))

def update_dzn_with_makespan(directory, solution_file):
    optimal_instances = load_optimal_instances(solution_file)
    
    for filename in os.listdir(directory):
        if filename in optimal_instances:
            path = os.path.join(directory, filename)
            with open(path, 'r') as file:
                content = file.read()

            if 'makespan' not in content:
                makespan = optimal_instances[filename]
                with open(path, 'a') as file:
                    file.write("makespan = " + str(makespan) + ";\n")
                print("Updated {} with makespan = {}".format(filename, makespan))
            else:
                print("Skipped {}: makespan already exists".format(filename))
        else:
            os.remove(os.path.join(directory, filename))
            print("Deleted {}: not optimal or not in solution file".format(filename))

# Example usage:
update_dzn_with_makespan("./dzn", "./Solutions.xlsx")
