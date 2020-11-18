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


def loader_activations(loader, model, layers):
    h = {}
    for k in layers.keys():
        h[k] = []

    for x, _ in loader:
        hx = activations(model, layers.values(), x)
        for i, k in enumerate(layers.keys()):
            h[k].append(hx[i])

    for k in layers.keys():
        h[k] = torch.cat(h[k])

    return h

def vae_layers(model):
    return {
        "mu": model.fc1,
        "logvar": model.fc2,
        "layer_1": model.encoder[0],
        "layer_2": model.encoder[2],
        "layer_4": model.encoder[4],
        "layer_6": model.encoder[6],
    }


def save_features(loader, model, epoch, out_paths):
    layers = vae_layers(model)
    h = loader_activations(loader, model, layers)

    # save these activations
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
