#!/usr/bin/env python
import torch
from torch import nn

class CBRNet(nn.Module):
    def __init__(self):
        super(CBRNet, self).__init__()

        self.cnn_layers = nn.Sequential(
            # Four layer fully convolutional net
            nn.Conv2d(3, 64, kernel_size=(5,5), stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(3,3), stride=(2,2),padding=1),

            nn.Conv2d(64, 128, kernel_size=(5,5), stride=1, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(3,3), stride=2, padding=1),

            nn.Conv2d(128, 256, kernel_size=(5,5), stride=1, padding=2),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(3,3), stride=2, padding=1),

            nn.Conv2d(256, 512, kernel_size=(5,5), stride=1, padding=2),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(3,3), stride=2, padding=1),

            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.linear_layers = nn.Sequential(
            nn.Linear(in_features=512, out_features=1, bias=True)
        )

    # Defining the forward pass
    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        return {"y_hat": self.linear_layers(x)}

def cnn_loss(x, y, output):
    l2 = torch.nn.MSELoss()
    return l2(output["y_hat"], y)