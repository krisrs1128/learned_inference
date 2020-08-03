"""
Train VAE on multichannel cell tiffs


python3 -m sim.vae -c conf/train.yaml
python3 -m sim.vae -c conf/train.yaml
"""
import argparse
import pathlib
import os
import yaml
from addict import Dict
from data import RandomCrop, CellDataset
from models.vae import VAE, loss_fn
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
    x, _, _ = next(iter(loader))
    x_hat, _, _ = model(x.to(device))
    writer.add_image("{stage}/x_hat", make_grid(x_hat), epoch)


def save_model(model, optim, epoch, out_dir):
    model_path = pathlib.Path(out_dir) / f"model_{epoch}.pt"
    optim_path = pathlib.Path(out_dir) / f"optim_{epoch}.pt"
    torch.save(model.state_dict(), model_path)
    torch.save(optim.state_dict(), optim_path)


def train(model, optim, loader, opts, out_dir, writer):
    """
    Wrap all training for a model
    """
    for epoch in range(opts.train.n_epochs):
        model, optim, losses = train_epoch(model, loader, optim, epoch)
        log_epoch(epoch, losses, loader, writer)

        if epoch % opts.train.save_every == 0:
            save_model(model, optim, epoch, out_dir)

    return losses


def train_epoch(model, loader, optim, epoch=0):
    """
    Train model for a single epoch
    """
    epoch_loss, i = 0, 0

    for x, _, _ in loader:
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

    for x, _, _ in loader:
        x = x.to(device)
        with torch.no_grad():
            z_mean, z_log_var, _, decoded = model(x)
            kl_divergence = (0.5 * (z_mean ** 2 + torch.exp(z_log_var) - z_log_var - 1)).sum()
            pixelwise_bce = F.binary_cross_entropy(decoded, x, reduction="sum")
            epoch_losses.append((kl_divergence + pixelwise_bce).item())

    return epoch_losses


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", type=str, help="configuration file")
    parser.add_argument("-b", "--boot", default=None, type=int, help="bootstrap index to run, with respect to file in config")
    args = parser.parse_args()
    opts = Dict(yaml.safe_load(open(args.conf)))

    data_dir = pathlib.Path(os.environ["DATA_DIR"])
    out_dir = data_dir / opts.organization.out_dir / str(args.boot)
    os.makedirs(out_dir, exist_ok=True)
    writer = SummaryWriter(out_dir / "logs")
    writer.add_text("conf", json.dumps(opts))

    # Setup model
    model = VAE(z_dim=opts.train.z_dim)
    optim = torch.optim.Adam(model.parameters(), lr=opts.train.lr)
    model.load_checkpoint(opts.train.checkpoint)

    # find indices to bootstrap on
    if args.boot is not None:
        resample_ix = pd.read_csv(data_dir / opts.bootstrap.path).iloc[args.boot].values
    else:
        resample_ix = None

    # train
    cell_data = CellDataset(
        data_dir / opts.organization.train_dir,
        data_dir / opts.organization.xy,
        RandomCrop(64),
        resample_ix
    )
    train_loader = DataLoader(cell_data, batch_size=opts.train.batch_size)
    train(model, optim, train_loader, opts, out_dir, writer)
