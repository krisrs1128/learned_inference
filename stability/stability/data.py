"""
Utilities for working with multichannel Tiffs

"""
import pathlib
import random
import os
import torch
from torch.utils.data import Dataset
import re
import pandas as pd
import numpy as np
from PIL import Image
import pandas as pd


def convert_dir_numpy(input_dir, output_dir):
    """
    Wrap tiff_to_numpy over an entire directory
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = list(pathlib.Path(input_dir).glob("*.tif"))
    for i, path in enumerate(paths):
        out_name = pathlib.Path(path).stem + ".npy"
        tiff_to_numpy(path, pathlib.Path(output_dir, out_name))


def save_pngs(input_dir, output_dir):
    """
    Save arrays as pngs, for easier viewing
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = list(pathlib.Path(input_dir).glob("*.npy"))
    for i, path in enumerate(paths):
        out_name = pathlib.Path(path).stem + ".png"
        im = Image.fromarray((255 * np.load(path)).astype(np.uint8))
        im.save(pathlib.Path(output_dir, out_name))


def random_split(ids, split_ratio):
    """
    Randomly split a list of paths into train / dev / test
    """
    random.shuffle(ids)
    sizes = len(ids) * np.array(split_ratio)
    ix = [int(s) for s in np.cumsum(sizes)]
    splits = {
        "train": ids[: ix[0]],
        "dev": ids[ix[0] : ix[1]],
        "test": ids[ix[1] : ix[2]],
    }

    splits_df = []
    for k in splits.keys():
        for v in splits[k]:
            splits_df.append({"path": v, "split": k})

    return pd.DataFrame(splits_df)


class CellDataset(Dataset):
    """
    Dataset for working with tiffs of cells
    """
    def __init__(self, img_paths, xy_path=None, root=pathlib.Path(".")):
        """Initialize dataset."""
        self.img_paths = img_paths
        self.root = root

        # default xy values
        if xy_path:
            self.xy = pd.read_csv(xy_path, index_col="path")
        else:
            self.xy = {"y": np.zeros(len(img_paths))}

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, i):
        img = np.load(self.root / self.img_paths[i])
        y = self.xy.loc[self.img_paths[i], "y"]
        return torch.Tensor(img.transpose(2, 0, 1)), torch.Tensor([y])
