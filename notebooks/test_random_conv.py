#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pathlib
from addict import Dict
from torch.utils.tensorboard import SummaryWriter
from stability.models.cnn import CBRNet
import stability.models.random_features as rcf
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
opts = Dict(yaml.safe_load(open(root_dir / "conf/cnn15.yaml", "r")))

features_dir = data_dir / opts.organization.features_dir
os.makedirs(features_dir, exist_ok=True)
writer = SummaryWriter(features_dir / "logs")
writer.add_text("conf", json.dumps(opts))


# In[ ]:


# build loaders
splits = pd.read_csv(data_dir / opts.organization.splits)
resample_ix = pd.read_csv(data_dir / opts.bootstrap.path)

paths = {
    "train": splits.loc[splits.split == "train", "path"].values,
    "dev": splits.loc[splits.split == "dev", "path"].values,
    "test": splits.loc[splits.split == "test", "path"].values
}


def initialize_loader(paths, data_dir, opts, **kwargs):
    cell_data = CellDataset(paths, data_dir / opts.organization.xy, data_dir)
    return DataLoader(cell_data, batch_size=opts.train.batch_size, **kwargs)

loaders = {}


# In[ ]:


p = [data_dir / s for s in paths["train"]]
patches = rcf.random_patches(p, k = 1024)
model = rcf.WideNet(torch.Tensor(patches))


# In[ ]:


patches2 = torch.Tensor(rcf.random_patches(p, 10))
D = model(patches2).detach()
D = D.squeeze()
max_ix = np.where(D[0, :] == D[0, :].max())[0][0]
print(max_ix)


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.imshow(np.transpose(patches[max_ix], (1, 2, 0)))
plt.show()
plt.imshow(np.transpose(patches2[0], (1, 2, 0)))


# In[ ]:


loaders["train"] = initialize_loader(paths["train"][resample_ix][0], data_dir, opts, shuffle=True)
loaders["features"] = initialize_loader(paths["train"], data_dir, opts)
loaders["dev"] = initialize_loader(paths["dev"], data_dir, opts)
loaders["test"] = initialize_loader(paths["test"], data_dir, opts)


# In[ ]:


l = loaders["train"]
l.dataset.root

i = 0
D = []
for x, _ in l:
    print(i)
    D.append(model(x))
    i += 1
    if i > 40:
        break


# In[ ]:


D = torch.cat(D).squeeze()


# In[ ]:


xy = pd.read_csv("/Users/kris/Documents/stability_data/Xy.csv")
y = xy.iloc[resample_ix.iloc[0, :]]["y"].values


# In[ ]:


import sklearn.linear_model as lm

ridge_model = lm.Ridge()
y = (y - y.mean()) / y.std()
ridge_model.fit(X = D.detach(), y = y[:len(D)])
ridge_model.coef_
y_hat = ridge_model.predict(X = D.detach())


# In[ ]:


plt.scatter(y[:len(D)], y_hat)


# In[ ]:




