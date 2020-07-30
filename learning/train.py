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
from torch.utils.data import DataLoader
import pandas as pd
import torch
import torch.nn.functional as F
from torchvision.utils import save_image
from models.vae import VAE, loss_fn
from data import RandomCrop, CellDataset, parse_env
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train(model, optim, loader, opts):
    """
    Wrap all training for a model
    """
    for epoch in range(opts.train.n_epochs):
        model, optim, losses = train_epoch(
            model,
            loader,
            optim,
            epoch,
            pathlib.Path(opts.organization.out_dir, "decodings")
        )
        print(f"epoch {epoch}: {losses}")

        if epoch % opts.save_every == 0:
            model_path = pathlib.Path(opts.organization.out_dir, f"model_{epoch}.pt")
            optim_path = pathlib.Path(opts.organization.out_dir, f"optim_{epoch}.pt")
            torch.save(model.state_dict(), model_path)
            torch.save(optim.state_dict(), optim_path)

    return losses


def train_epoch(model, loader, optim, epoch=0, im_dir=pathlib.Path(".")):
    """
    Train model for a single epoch
    """
    os.makedirs(im_dir, exist_ok=True)
    epoch_loss, i = 0, 0

    for x, _, _ in loader:
        # get loss
        x = x.to(device)
        x_hat, mu, logvar = model(x)
        loss, bce, kld = loss_fn(x_hat, x, mu, logvar)

        # update
        optim.zero_grad()
        loss.backward()
        optim.step()
        epoch_loss += loss.item()

        if i < 1:
            save_image(x_hat, im_dir / f"decoded_{str(i)}_{epoch}.png")
        i += 1

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
    opts.organization = parse_env(opts.organization)

    data_dir = pathlib.Path(os.environ["DATA_DIR"])
    os.makedirs(data_dir / opts.organization.out_dir, exist_ok=True)

    # training
    model = VAE(z_dim=opts.train.z_dim)
    optim = torch.optim.Adam(model.parameters(), lr=opts.train.lr)

    if args.boot:
        args.boot = pd.read_csv(data_dir / opts.bootstrap.path).iloc[args.boot, -1] # skip index col

    cell_data = CellDataset(
        data_dir / opts.organization.train_dir,
        data_dir / opts.organization.xy,
        RandomCrop(64),
        args.boot
    )
    train_loader = DataLoader(cell_data, batch_size=opts.train.batch_size)
    train(model, optim, train_loader, opts)
