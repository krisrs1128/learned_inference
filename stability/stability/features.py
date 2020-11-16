"""
Save features from trained model

Usage:
python3 -m features -c ../conf/train.yaml
"""
import numpy as np
import os
from addict import Dict
from pathlib import Path
from torch.utils.data import DataLoader
import argparse
import pandas as pd
import torch
import yaml


class SaveOutput:
    def __init__(self):
        self.outputs = []

    def __call__(self, module, module_in, module_out):
        self.outputs.append(module_out)

    def clear(self):
        self.outputs = []


def activations(model, layers, x, device=None):
    """Get all activation vectors over images for a model.
    :param model: A pytorch model
    :type model: currently is Net defined by ourselves
    :param layers: One or more layers that activations are desired
    :type layers: torch.nn.modules.container.Sequential
    :param x: A 4-d tensor containing the test datapoints from which activations are desired.
                The 1st dimension should be the number of test datapoints.
                The next 3 dimensions should match the input of the model
    :type x: torch.Tensor
    :return (output): A list containing activations of all specified layers.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    save_output = SaveOutput()
    hook_handles = []

    for layer in layers:
        handle = layer.register_forward_hook(save_output)
        hook_handles.append(handle)

    with torch.no_grad():
      x = x.to(device)
      out = model(x)

    output = save_output.outputs.copy()
    del save_output, hook_handles, out
    return output


def save_features(loader, model, layers, epoch, out_paths):
    """
    To save in python and load in R, can use

    Python >
    h = save_features(ft_loader, model, layers, "0", "tmp")
    np.save("h1.npy", h["layer_1"].numpy())

    R >
    library("reticulate")
    np <- import("numpy", convert=FALSE)
    h <- py_to_r(np$load("h1.npy"))
    """
    h = {}
    for i in range(len(layers)):
        h[f"layer_{i}"] = []

    for x, _ in loader:
        hx = activations(model, layers, x[:, :, :64, :64])
        for i, l in enumerate(layers):
            h[f"layer_{i}"].append(hx[i])

    for i in range(len(layers)):
        h[f"layer_{i}"] = torch.cat(h[f"layer_{i}"])

    return h


def save_encodings(loader, model, model_path, out_path):
    os.makedirs(out_path.parent, exist_ok=True)

    i = 0
    for x, y, img_id, img_path in loader:
        batch_size = len(x)
        mode = "w" if i == 0 else "a"

        with torch.no_grad():
            z_mean, _, _ = model.encode(x)
            z_mean = np.array(z_mean)
            z_df = pd.DataFrame(z_mean)
            z_df["model"] = model_path
            z_df["img_id"] = img_id[0]
            z_df["path"] = img_path[0]
            z_df["y"] = np.array(y)
            z_df.to_csv(out_path, mode=mode, header=(i == 0))

        i += 1


def save_wrapper(loader, model, model_paths, out_dir):
    for model_path in model_paths:
        print(f"Saving features for {model_path}")
        model.load_state_dict(torch.load(model_path))
        out_path = out_dir / Path(f"features_{model_path.parts[-2]}.csv")
        save_encodings(loader, model, model_path, out_path)
