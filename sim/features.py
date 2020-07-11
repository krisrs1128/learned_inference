"""
Save features from trained model

Usage:
python3 -m sim.features -c conf/train.yaml -m data/runs/vae_100/model_190.pt
"""
import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import yaml
from addict import Dict
import torch
import os
from torch.utils.data import DataLoader
from models.vae import VariationalAutoencoder
import sim.data as dt


def save_encodings(loader, model, out_path):
    os.makedirs(out_path.stem, exist_ok=True)

    i = 0
    for x in loader:
        batch_size = len(x)
        mode = "w" if i == 0 else "a"

        with torch.no_grad():
            z_mean, _, _ = model.encode(x)
            z_mean = np.array(z_mean)
            z_df = pd.DataFrame(z_mean)
            z_df["path"] = loader.dataset.img_files[i:(i + batch_size)]
            z_df.to_csv(out_path, mode=mode, header=(i == 0))

        i += batch_size


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", type=str, help="configuration file")
    parser.add_argument("-m", "--model_path", type=str, help="path to saved model")
    args = parser.parse_args()
    opts = Dict(yaml.safe_load(open(args.conf)))

    model = VariationalAutoencoder(n_latent=opts.n_latent)
    model.load_state_dict(torch.load(args.model_path))

    cell_data = dt.CellDataset(opts.train_dir, dt.RandomCrop(96))
    train_loader = DataLoader(cell_data, batch_size=opts.batch_size)
    save_encodings(train_loader, model, Path(opts.features_dir))
