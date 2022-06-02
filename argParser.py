import sys
import json

def findById(id, dictionary):
    for _ , value in dictionary.items():
        if value["id"] == id:
            return value
    sys.exit("Identification value not found: {}".format(id))

def getBenchmarkSolverTimeout(args):
    b, s, t = _getBenchmarkSolversTimeout(args.b, [args.s], args.t, ".")
    return (b, s[0], t)

def getBenchmarkSolversTimeout(args, path):
    return _getBenchmarkSolversTimeout(args.b, args.s, args.t, path)

def _getBenchmarkSolversTimeout(b, s, t, path):
    benchmarks_file = open("{}/benchmarks.json".format(path), "r")
    benchmarks_info = json.load(benchmarks_file)
    benchmarks_file.close()
    solvers_file = open("{}/solvers.json".format(path), "r")
    solvers_info = json.load(solvers_file)
    solvers_file.close()
    benchmark = findById(b, benchmarks_info)
    solvers = [findById(_s,solvers_info) for _s in s]
    return (benchmark, solvers, int(t))

