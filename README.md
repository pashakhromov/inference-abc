# inference-abc

Part of my PhD project related to inferring distribution of evolutionary parameters of *D. megalonaster* along the DNA using Approximate Bayesian Computation (ABC). See https://rucore.libraries.rutgers.edu/rutgers-lib/64352/ for details.

Order of runs
1. `run_seqstats.sh` turns raw `fasta` data into relevant stats
2. `run_hist.sh` turns these relevant stats into ABC digestable observable
3. `run_infer.sh` does the inference returning posterior
