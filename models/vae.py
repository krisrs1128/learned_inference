"""


mostly copied from: https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/autoencoder/ae-var.ipynb
"""
import torch
from torch import nn
import pathlib
import os
import sim.data as dt
from torch.utils.data import DataLoader
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class VariationalAutoencoder(torch.nn.Module):
    def __init__(self, n_latent=100, negative_slope=0.0001):
        super(VariationalAutoencoder, self).__init__()

        ### ENCODER
        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=1, stride=1, padding=0),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=4, padding=1),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=4, padding=1),
            nn.LeakyReLU(negative_slope=negative_slope),
        )

        self.z_mean = nn.Linear(256 * 6 * 6, n_latent)
        self.z_log_var = nn.Linear(256 * 6 * 6, n_latent)

        ### DECODER
        self.dec_linear = nn.Linear(n_latent, 256 * 6 * 6)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=1, stride=1),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=4, stride=4),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.ConvTranspose2d(in_channels=64, out_channels=32, kernel_size=4, stride=4),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.ConvTranspose2d(in_channels=32, out_channels=3, kernel_size=1, stride=1),
            nn.LeakyReLU(negative_slope=negative_slope),
        )

    def reparameterize(self, z_mu, z_log_var):
        # Sample epsilon from standard normal distribution
        eps = torch.randn(z_mu.size(0), z_mu.size(1)).to(device)
        # note that log(x^2) = 2*log(x); hence divide by 2 to get std_dev
        # i.e., std_dev = exp(log(std_dev^2)/2) = exp(log(var)/2)
        return z_mu + eps * torch.exp(z_log_var/2.)

    def encode(self, x):
        x = self.encoder(x)
        z_mean = self.z_mean(x.view(-1, 256 * 6 * 6))
        z_log_var = self.z_log_var(x.view(-1, 256 * 6 * 6))
        encoded = self.reparameterize(z_mean, z_log_var)
        return z_mean, z_log_var, encoded

    def decode(self, z):
        x = self.dec_linear(z)
        x = x.view(-1, 256, 6, 6)
        x = self.decoder(x)
        return torch.sigmoid(x)

    def forward(self, x):
        z_mean, z_log_var, encoded = self.encode(x)
        decoded = self.decode(encoded)
        return z_mean, z_log_var, encoded, decoded


if __name__ == '__main__':
    npy_dir = pathlib.Path(os.environ["ROOT_DIR"], "data", "npys")
    data = dt.CellDataset(npy_dir, dt.RandomCrop(96))

    vae = VariationalAutoencoder()

    loader = DataLoader(data, batch_size=32)
    for x in loader:
        z_mean, z_var, encoded, decoded = vae.forward(x)
