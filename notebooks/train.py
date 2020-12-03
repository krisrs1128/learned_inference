#!/usr/bin/env python
# coding: utf-8
"""
Load Splits and Train Models

This is a wrapper that helps us run a few types of models on a few splits of
data. The outputs of this script are (1) saved features and (2) a trained model,
selected to have the best dev set score.
"""
import argparse
import os
import json
import pathlib
from addict import Dict
from stability.data import initialize_loader
from stability.models.vae import VAE, vae_loss
from stability.models.cnn import CBRNet, cnn_loss
from torch.utils.tensorboard import SummaryWriter
import numpy as np
import pandas as pd
import stability.train as st
import torch
import torch.optim
import yaml


parser = argparse.ArgumentParser(description="Preprocess raw tiffs into slices")
parser.add_argument("-c", "--train_yaml", default="../conf/train_cnn.yaml", type=str)
parser.add_argument("-b", "--bootstrap", default=0, type=int)
args = parser.parse_args()

data_dir = pathlib.Path(os.environ["DATA_DIR"])
root_dir = pathlib.Path(os.environ["ROOT_DIR"])
opts = Dict(yaml.safe_load(open(root_dir / args.train_yaml, "r")))

features_dir = data_dir / opts.organization.features_dir
os.makedirs(features_dir, exist_ok=True)

# Setup model
print(opts.train)
if opts.train.model == "cnn":
    model = CBRNet()
    loss_fn = cnn_loss
elif opts.train.model == "vae":
    model = VAE(z_dim=opts.train.z_dim)
    loss_fn = vae_loss
elif opts.train.model == "rcf":
    raise NotImplementedError()
else:
    raise NotImplementedError()

# build loaders
splits = pd.read_csv(data_dir / opts.organization.splits)
resample_ix = pd.read_csv(data_dir / opts.bootstrap.path)

paths = {
    "train": splits.loc[splits.split == "train", "path"].values[resample_ix],
    "dev": splits.loc[splits.split == "dev", "path"].values,
    "test": splits.loc[splits.split == "test", "path"].values,
    "all": splits["path"].values
}

save_ix = np.random.choice(len(splits), opts.train.save_subset, replace=False)
loaders = {
    "train_fixed": initialize_loader(paths["train"][args.bootstrap], data_dir, opts),
    "train": initialize_loader(paths["train"][args.bootstrap], data_dir, opts, shuffle=True),
    "dev": initialize_loader(paths["dev"], data_dir, opts),
    "test": initialize_loader(paths["test"], data_dir, opts),
    "features": initialize_loader(paths["all"][save_ix], data_dir, opts)
}

# prepare logging
subset_path = data_dir / opts.organization.features_dir / "subset.csv"
splits.iloc[save_ix, :].to_csv(subset_path)
writer = SummaryWriter(features_dir / "logs")
writer.add_text("conf", json.dumps(opts))
out_paths = [
    data_dir / opts.organization.features_dir,
    data_dir / opts.organization.metadata,
    data_dir / opts.organization.model
]

# train
optim = torch.optim.Adam(model.parameters(), lr=opts.train.lr)
st.train(model, optim, loaders, opts, out_paths, writer, loss_fn)
