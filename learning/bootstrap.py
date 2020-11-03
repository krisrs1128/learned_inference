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
