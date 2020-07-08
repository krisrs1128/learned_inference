"""


mostly copied from: https://github.com/rasbt/deeplearning-models/blob/master/pytorch_ipynb/autoencoder/ae-var.ipynb
"""
import torch
from torch import nn

class VariationalAutoencoder(torch.nn.Module):
    def __init__(self, n_input, n_hiddens, n_latent, negative_slope=0.0001):
        super(VariationalAutoencoder, self).__init__()

        ### ENCODER
        self.encoder = nn.Sequential(
            nn.Linear(n_input, n_hiddens[0]),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Linear(n_hiddens[0], n_hiddens[1]),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Linear(n_hiddens[1], n_hiddens[2])
        )

        self.z_mean = nn.Linear(n_hiddens[-1], n_latent)
        self.z_log_var = nn.Linear(n_hiddens[-1], n_latent)

        ### DECODER
        self.decoder = nn.Sequential(
            nn.Linear(n_latent, n_hiddens[2]),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Linear(n_hiddens[2], n_hiddens[1]),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Linear(n_hiddens[1], n_hiddens[0]),
            nn.LeakyReLU(negative_slope=negative_slope),
            nn.Linear(n_hiddens[0], n_input)
        )

    def reparameterize(self, z_mu, z_log_var):
        # Sample epsilon from standard normal distribution
        eps = torch.randn(z_mu.size(0), z_mu.size(1)).to(device)
        # note that log(x^2) = 2*log(x); hence divide by 2 to get std_dev
        # i.e., std_dev = exp(log(std_dev^2)/2) = exp(log(var)/2)
        return z_mu + eps * torch.exp(z_log_var/2.)

    def encoder(self, x):
        x = self.encoder(x)
        z_mean = self.z_mean(x)
        z_log_var = self.z_log_var(x)
        encoded = self.reparameterize(z_mean, z_log_var)
        return z_mean, z_log_var, encoded

    def decoder(self, z):
        x = self.decoder(z)
        decoded = torch.sigmoid(x)
        return decoded

    def forward(self, x):
        z_mean, z_log_var, encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return z_mean, z_log_var, encoded, decoded
