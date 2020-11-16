"""
Train VAE on multichannel cell tiffs

python3 -m train -c ../conf/train.yaml
"""
import argparse
import pathlib
import os
import yaml
from addict import Dict
from .data import CellDataset
from .models.vae import VAE, loss_fn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision.utils import make_grid
from torchvision.utils import save_image
import json
import pandas as pd
import torch
import torch.nn.functional as F
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def log_epoch(epoch, loss, loader, writer, stage="train"):
    writer.add_scalar(f"{stage}/loss", loss, epoch)
    x, _, _, _ = next(iter(loader))
    x_hat, _, _ = model(x.to(device))
    writer.add_image("{stage}/x_hat", make_grid(x_hat), epoch)


def train(model, optim, loaders, opts, out_paths, writer):
    """
    Wrap all training for a model
    """
    for epoch in range(opts.train.n_epochs):
        model, optim, losses = train_epoch(model, loader, optim, epoch)
        log_epoch(epoch, losses, loaders["train"], writer)

        if epoch % opts.train.save_every == 0:
            save_features(loaders["features"], model, epoch, out_paths)

    save_features(loaders["features"], model, "final", out_paths)
    return losses


def train_epoch(model, loader, optim, epoch=0):
    """
    Train model for a single epoch
    """
    epoch_loss, i = 0, 0

    for x, _, _, _ in loader:
        # get loss
        x = x.to(device)
        x_hat, mu, logvar = model(x)
        loss, _, _ = loss_fn(x_hat, x, mu, logvar)

        # update
        optim.zero_grad()
        loss.backward()
        optim.step()
        epoch_loss += loss.item()

    return model, optim, epoch_loss / len(loader)


def losses(model, loader):
    """
    Calculate losses on an arbitrary loader
    """
    epoch_losses = []

    for x, _, _, _ in loader:
        x = x.to(device)
        with torch.no_grad():
            z_mean, z_log_var, _, decoded = model(x)
            loss = loss_fn(x_hat, x, z_mean, z_var)[0]
            epoch_losses.append(loss.item())

    return epoch_losses
