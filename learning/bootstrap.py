"""
Organize and Launch many VAE runs

python3 -m sim.bootstrap -c conf/bootstrap.yaml
"""
import pandas as pd
import numpy as np

# read the configuration file specifying number of bootstraps and folder to save everything
# generate bootstrap indices, and save them to a csv that can be read by tibble
# for i in 1 to n_bootstraps
# define the configuration file for the i^th training run
# define the sbatch script for training on that sample
# make sure to specify the directory structure where the outputs will be saved
# make sure to specify which of the bootstrap indices the sbatched model will be using
# save the results to some directory

def bootstrap_indices(N, B=30, out_path):
    pass

def write_sbatch(index, config, out_dir):
    pass

def launch_jobs(path):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", type=str, help="configuration file")
    args = parser.parse_args()
    opts = Dict(yaml.safe_load(open(args.conf)))
