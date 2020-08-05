"""
Save features from trained model

Usage:
python3 -m features -c ../conf/train.yaml
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
from models.vae import VAE
import data as dt


def save_encodings(loader, model, out_path):
    os.makedirs(out_path.parent, exist_ok=True)

    i = 0
    for x, y, img_path in loader:
        batch_size = len(x)
        mode = "w" if i == 0 else "a"

        with torch.no_grad():
            z_mean, _, _ = model.encode(x)
            z_mean = np.array(z_mean)
            z_df = pd.DataFrame(z_mean)
            z_df["path"] = img_path[0]
            z_df["y"] = np.array(y)
            z_df.to_csv(out_path, mode=mode, header=(i == 0))

        i += 1

def save_wrapper(loader, model, model_paths, out_dir):
    for model_path in model_paths:
        print(f"Saving features for {model_path}")
        model.load_state_dict(torch.load(model_path))
        out_path = out_dir / Path(f"features_{model_path.parts[-2]}.csv")
        save_encodings(loader, model, out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", type=str, help="configuration file")
    parser.add_argument("-m", "--models_dir", type=str, help="directory containing model")
    args = parser.parse_args()
    opts = Dict(yaml.safe_load(open(args.conf)))

    model = VAE(z_dim=opts.train.z_dim)
    data_dir = Path(os.environ["DATA_DIR"])
    cell_data = dt.CellDataset(
        data_dir / opts.organization.train_dir,
        data_dir / Path(opts.organization.xy),
        dt.RandomCrop(64)
    )
    train_loader = DataLoader(cell_data, batch_size=opts.train.batch_size)

    if opts.bootstrap.B is None:
        model_paths = [data_dir / opts.organization.out_dir / "None" / "model_70.pt"]
    else:
        model_paths = [data_dir / opts.organization.out_dir / str(b) / "model_70.pt" for b in range(opts.bootstrap.B)]

    save_wrapper(
        train_loader,
        model,
        model_paths,
        data_dir / opts.organization.features_dir
    )
