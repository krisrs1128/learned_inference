"""
Organize and Launch many VAE runs

python3 -m learning.bootstrap -c conf/train.yaml
"""
import pandas as pd
import numpy as np
import argparse
import pathlib
import os
from addict import Dict
import yaml

# read the configuration file specifying number of bootstraps and folder to save everything
# generate bootstrap indices, and save them to a csv that can be read by tibble
# for i in 1 to n_bootstraps
# define the configuration file for the i^th training run
# define the sbatch script for training on that sample
# make sure to specify the directory structure where the outputs will be saved
# make sure to specify which of the bootstrap indices the sbatched model will be using
# save the results to some directory

def bootstrap_indices(N, B=30, out_path="./"):
    result = np.zeros((B, N))
    for b in range(B):
        result[b, :] = np.random.choice(range(N), N)

    os.makedirs(out_path.parent, exist_ok=True)
    result = result.astype(int)
    pd.DataFrame(result).to_csv(out_path)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", type=str, help="configuration file")
    args = parser.parse_args()
    opts = Dict(yaml.safe_load(open(args.conf)))

    data_dir = pathlib.Path(os.environ["DATA_DIR"])
    out_path = pathlib.Path(data_dir / opts.bootstrap.path)
    train_imgs = list(pathlib.Path(data_dir / opts.organization.train_dir).glob("*npy"))
    bootstrap_indices(len(train_imgs), opts.bootstrap.B, out_path)
