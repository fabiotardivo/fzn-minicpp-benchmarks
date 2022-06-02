MiniCPP-Benchmarks
==
Benchmarks for MiniCPP in MiniZinc format. Each benchmark includes:

- A README.md file containing: problem description, origin of the dataset, references.
- A commented MiniZinc model.
- Multiple DataZinc files of small, medium and big size.

It also includes some python scripts to help the benchmarking process:

- [runBenchmarks.py](./runBenchmarks.py): Runs and logs the benchmarks.
- [log2csv.py](./log2csv.py): Generate tabular data from the logs.

Benchmarks for GPU-accelerated constraint propagation
--

- [Resource Constrained Project Scheduling Problem](./rcpsp): Used to test the propagation of the Cumulative constraint.
