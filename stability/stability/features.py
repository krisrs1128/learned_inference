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


def load_checkpoint(model, path, load_keys=None):
    """
    Load from a subset of keys
    """
    if torch.cuda.is_available():
        pretrained = torch.load(path)
    else:
        pretrained = torch.load(path, map_location=torch.device("cpu"))

    state = model.state_dict()
    if load_keys is None:
      load_keys = state.keys()

    state_subset = {k: v for k, v in prtrained.items() if k in load_keys}
    state.update(state_subset)
    self.load_state_dict(state)


def activations(model, prefixes, x):
    """Get all activation vectors over images for a model.
    :param model: A pytorch model
    :type model: currently is Net defined by ourselves
    :param prefixes: One or more prefixes that activations are desired
    :type prefixes: torch.nn.Module
    :param x: A 4-d tensor containing the test datapoints from which activations are desired.
                The 1st dimension should be the number of test datapoints.
                The next 3 dimensions should match the input of the model
    :type x: torch.Tensor
    :return (output): A list containing activations of all specified prefixes.
    """
    with torch.no_grad():
      output = model(x)
    return output


def loader_activations(loader, model, prefixes, device):
    h = {}
    for k in prefixes.keys():
        h[k] = []

    for x, _ in loader:
        hx = activations(model.to(device), prefixes.values(), x.to(device))
        for i, k in enumerate(prefixes.keys()):
            h[k].append(hx[i])

    for k in prefixes.keys():
        h[k] = torch.cat(h[k])

    return h


def vae_prefixes(model):
    return {
        "layer_1": model.encoder[0],
        "layer_2": model.encoder[:2],
        "layer_3": model.encoder[:4],
        "layer_4": model.encoder[:6],
        "mu": model.fc1,
        "logvar": model.fc2
    }


def cbr_prefixes(model):
    return {
        "layer_1": model.cnn_prefixes[:3],
        "layer_2": model.cnn_prefixes[:7],
        "layer_3": model.cnn_prefixes[:11],
        "layer_4": model.cnn_prefixes[:15],
        "linear": model.cnn_prefixes,
        "final": model
    }


def save_features(loader, model, epoch, out_paths):
    if "VAE" in str(model.__class__):
        prefixes = vae_prefixes(model)
    else:
        prefixes = cbr_prefixes(model)

    # save these activations
    h = loader_activations(loader, prefixes)
    metadata = []
    for k in h.keys():
        k_path = Path(out_paths[0]) / f"{k}_{str(epoch)}.npy"
        if not k_path.parent.exists():
            k_path.parent.mkdir(parents=True, exist_ok=True)

        np.save(k_path, h[k].detach().cpu().numpy())
        metadata.append({"epoch": epoch, "layer": k, "out_path": k_path})

    # save relevant metadata
    metadata = pd.DataFrame(metadata)
    if Path(out_paths[1]).exists():
        metadata.to_csv(out_paths[1], mode="a", header=False)
    else:
        metadata.to_csv(out_paths[1])

    return h
