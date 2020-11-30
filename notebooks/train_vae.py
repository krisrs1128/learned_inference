#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pathlib
from addict import Dict
from torch.utils.tensorboard import SummaryWriter
from stability.models.vae import VAE
from stability.data import CellDataset
import stability.train as st
import torch.optim
from torch.utils.data import DataLoader, Subset
import yaml
import torch
import os
import numpy as np
import pandas as pd
import json


# In[ ]:


data_dir = pathlib.Path(os.environ["DATA_DIR"])
 root_dir = pathlib.Path(os.environ["ROOT_DIR"])
opts = Dict(yaml.safe_load(open(root_dir / "conf/train_vae.yaml", "r")))

features_dir = data_dir / opts.organization.features_dir
os.makedirs(features_dir, exist_ok=True)
writer = SummaryWriter(features_dir / "logs")
writer.add_text("conf", json.dumps(opts))


# In[ ]:


# Setup model
model = VAE(z_dim=opts.train.z_dim)
optim = torch.optim.Adam(model.parameters(), lr=opts.train.lr)
if opts.train.checkpoint is not None:
    model.load_checkpoint(data_dir / opts.train.checkpoint)

# build loaders
splits = pd.read_csv(data_dir / opts.organization.splits)
resample_ix = pd.read_csv(data_dir / opts.bootstrap.path)

paths = {
    "train": splits.loc[splits.split == "train", "path"].values,
    "dev": splits.loc[splits.split == "dev", "path"].values,
    "test": splits.loc[splits.split == "test", "path"].values
}


def initialize_loader(paths, data_dir, opts, **kwargs):
    cell_data = CellDataset(paths, data_dir / opts.organization.xy)
    return DataLoader(cell_data, batch_size=opts.train.batch_size, **kwargs)

loaders = {}
loaders["train"] = initialize_loader(paths["train"][resample_ix][0], data_dir, opts, shuffle=True)
loaders["features"] = initialize_loader(paths["train"], data_dir, opts)
loaders["dev"] = initialize_loader(paths["dev"], data_dir, opts)
loaders["test"] = initialize_loader(paths["test"], data_dir, opts)

# train
out_paths = [data_dir / opts.organization.features_dir, data_dir / opts.organization.metadata]
st.train(model, optim, loaders, opts, out_paths, writer)


# In[ ]:




