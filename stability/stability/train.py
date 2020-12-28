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
from .models.vae import vae_loss
import numpy as np
import os
import pandas as pd
import pathlib
import torch
import torch.nn.functional as F
import yaml


def log_stage(stage, epoch, model, loss, loader, writer, device):
    writer.add_scalar(f"loss/{stage}", np.mean(loss[epoch]), epoch)
    x, _ = next(iter(loader))

    if "VAE" in str(model.__class__):
      x_hat  = model(x.to(device))["x_hat"]
      writer.add_image(f"x_hat/{stage}", make_grid(x_hat), epoch)
    else:
      y_hat = model(x.to(device))["y_hat"]
      for i in range(len(y_hat)):
          writer.add_scalar(f"y_hat_{i}/{stage}", y_hat[i], epoch)


def log_epoch(epoch, model, loss, loaders, writer, device):
    log_stage("train", epoch, model, loss["train"], loaders["train_fixed"], writer, device)
    log_stage("dev", epoch, model, loss["dev"], loaders["dev"], writer, device)


def train(model, optim, loaders, opts, out_paths, writer, loss_fn=vae_loss):
    """
    Wrap all training for a model
    """
    loss = {"dev": [], "train": []}
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    scheduler = ReduceLROnPlateau(optim, mode="max", factor=0.5, patience=2)

    for epoch in range(opts.train.n_epochs):
        model, optim, lt = train_epoch(model, loaders["train"], optim, loss_fn, device)
        loss["train"].append(lt)
        loss["dev"].append(losses(model, loaders["dev"], loss_fn))
        log_epoch(epoch, model, loss, loaders, writer, device)

        # periodically save features
        if epoch % opts.train.save_every == 0 or (epoch + 1) == opts.train.n_epochs:
            save_features(loaders["features"], model, epoch, out_paths, device)

        # save best features / model
        if loss["dev"][-1] == min(loss["dev"]):
            save_features(loaders["features"], model, "best", out_paths, device)
            torch.save(model.state_dict(), out_paths[2])

        print(f"{epoch}/{opts.train.n_epochs} | train: {loss['train'][-1]} | dev: {loss['dev'][-1]} |")
        scheduler.step(loss["dev"][-1])
    return loss


def train_epoch(model, loader, optim, loss_fn, device):
    """
    Train model for a single epoch
    """
    epoch_losses, i = [], 0
    model = model.to(device)

    for x, y, in loader:
        # get loss
        x = x.to(device)
        y = y.to(device)
        output = model(x)
        loss = loss_fn(x, y, output)

        # update
        optim.zero_grad()
        loss.backward()
        optim.step()
        epoch_losses.append(loss.cpu().item())

    return model, optim, epoch_losses


def losses(model, loader, loss_fn=vae_loss):
    """
    Calculate losses on an arbitrary loader
    """
    epoch_losses = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for x, y in loader:
        x = x.to(device)
        y = y.to(device)
        model.eval()
        with torch.no_grad():
            output = model(x)
            loss = loss_fn(x, y, output)
            epoch_losses.append(loss.cpu().item())

    return epoch_losses
