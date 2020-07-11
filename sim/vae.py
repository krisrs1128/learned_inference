"""
Train VAE on multichannel cell tiffs
"""
import torch
from torch.utils.data import DataLoader, Dataset
import pathlib
import time
import yaml
import argparse
from addict import Dict
import sim.data as dt
import torch.nn.functional as F
import os
from models.vae import VariationalAutoencoder
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train(model, optim, loader, opts):
    for epoch in range(opts.n_epochs):
        model, optim, losses = train_epoch(model, loader, optim)
        print(f"epoch {epoch}: {losses}")

        if epoch % opts.save_every == 0:
            model_path = pathlib.Path(opts.out_dir, f"model_{epoch}.pt")
            optim_path = pathlib.Path(opts.out_dir, f"optim_{epoch}.pt")
            torch.save(model.state_dict(), model_path)
            torch.save(optim.state_dict(), optim_path)

    return losses


def train_epoch(model, loader, optim):
    epoch_loss = 0

    for i, x in enumerate(loader):
        # get loss
        x = x.to(device)
        z_mean, z_log_var, _, decoded = model(x)
        kl_divergence = (0.5 * (z_mean ** 2 + torch.exp(z_log_var) - z_log_var - 1)).sum()
        pixelwise_bce = F.binary_cross_entropy(decoded, x, reduction="sum")
        loss = kl_divergence + pixelwise_bce

        # update
        optim.zero_grad()
        loss.backward()
        optim.step()
        epoch_loss += loss.item()

    return model, optim, epoch_loss


def losses(model, loader):
    epoch_losses = []

    for i, x in enumerate(loader):
        x = x.to(device)
        with torch.no_grad():
            z_mean, z_log_var, _, decoded = model(features)
            kl_divergence = (0.5 * (z_mean ** 2 + torch.exp(z_log_var) - z_log_var - 1)).sum()
            pixelwise_bce = F.binary_cross_entropy(decoded, features, reduction="sum")
            epoch_losses.append((kl_divergence + pixelwise_bce).item())

    return epoch_loss


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", type=str, help="configuration file")
    args = parser.parse_args()
    opts = Dict(yaml.safe_load(open(args.conf)))
    os.makedirs(opts.out_dir, exist_ok=True)

    # training
    model = VariationalAutoencoder(n_latent=opts.n_latent)
    optim = torch.optim.Adam(model.parameters(), lr=opts.lr)
    cell_data = dt.CellDataset(opts.train_dir, dt.RandomCrop(96))
    train_loader = DataLoader(cell_data, batch_size=opts.batch_size)
    train(model, optim, train_loader, opts)
