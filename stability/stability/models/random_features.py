#!/usr/bin/env python
import torch
import torch.nn.functional as F
from torch import nn

class ConvSubset(nn.Module):
    def __init__(self, patches):
        super(ConvSubset, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.conv = nn.Conv2d(3, len(patches), patches.shape[2], bias=False)
        self.conv.weight = nn.Parameter(patches.to(self.device))

    def forward(self, x):
        return self.conv(x)


class WideNet(nn.Module):
    def __init__(self, patches):
        super(WideNet, self).__init__()
        self.patches = patches
        self.filter_subset = 1024

    def forward(self, x):
        h = []
        for i in range(0, len(self.patches), self.filter_subset):
            h_cur = self.forward_partial(x, i, i + self.filter_subset)
            h.append(h_cur)

        return torch.cat(h, dim=1)

    def forward_partial(self, x, start, end):
        conv = ConvSubset(self.patches[start:end])
        pre_h = conv(x)
        return F.max_pool2d(F.relu(pre_h - 1), pre_h.shape[2])
