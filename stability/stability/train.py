"""
Train VAE on multichannel cell tiffs

python3 -m train -c ../conf/train.yaml
"""
from addict import Dict
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision.utils import make_grid
from torchvision.utils import save_image
from .features import save_features
from .models.vae import loss_fn
import numpy as np
import os
import pandas as pd
import pathlib
import torch
import torch.nn.functional as F
import yaml


def log_stage(stage, epoch, model, loss, loader, writer):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    writer.add_scalar(f"loss/{stage}", np.mean(loss[epoch]), epoch)
    x, _ = next(iter(loader))
    x_hat, _, _ = model(x.to(device))
    writer.add_image(f"x_hat/{stage}", make_grid(x_hat), epoch)


def log_epoch(epoch, model, loss, loaders, writer):
    log_stage("train", epoch, model, loss["train"], loaders["train"], writer)
    log_stage("dev", epoch, model, loss["dev"], loaders["dev"], writer)


def train(model, optim, loaders, opts, out_paths, writer):
    """
    Wrap all training for a model
    """
    loss = {"dev": [], "train": []}
    for epoch in range(opts.train.n_epochs):
        model, optim, lt = train_epoch(model, loaders["train"], optim)
        loss["train"].append(lt)
        loss["dev"].append(losses(model, loaders["dev"]))
        log_epoch(epoch, model, loss, loaders, writer)

        if epoch % opts.train.save_every == 0 or (epoch + 1) == opts.train.n_epochs:
            save_features(loaders["features"], model, epoch, out_paths)

    return loss


def train_epoch(model, loader, optim):
    """
    Train model for a single epoch
    """
    epoch_losses, i = [], 0
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for x, _, in loader:
        # get loss
        x = x.to(device)
        x_hat, mu, logvar = model(x)
        loss, _, _ = loss_fn(x_hat, x, mu, logvar)

        # update
        optim.zero_grad()
        loss.backward()
        optim.step()
        epoch_losses.append(loss.item())

    return model, optim, epoch_losses


def losses(model, loader):
    """
    Calculate losses on an arbitrary loader
    """
    epoch_losses = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for x, _ in loader:
        x = x.to(device)
        with torch.no_grad():
            x_hat, mu, logvar = model(x)
            loss = loss_fn(x_hat, x, mu, logvar)[0]
            epoch_losses.append(loss.item())

    return epoch_losses
