"""
Utilities for working with multichannel Tiffs

"""
import pathlib
import random
import os
from shutil import copyfile
import torch
from torch.utils.data import Dataset
import rasterio
import re
import pandas as pd
import numpy as np
from PIL import Image
import pandas as pd


def tiff_to_numpy(input_path, output_path):
    """
    Save a tiff image as a numpy array
    """
    imgf = rasterio.open(input_path)
    img = imgf.read().transpose(1, 2, 0)
    np.save(str(output_path), img)


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
    return {
        "train": ids[: ix[0]],
        "dev": ids[ix[0] : ix[1]],
        "test": ids[ix[1] : ix[2]],
    }


def reshuffle(split_ids, output_dir="output/", n_cpu=3):
    """
    Reshuffle Data for Training

    Given a dictionary specifying train / dev / test split, copy into train /
    dev / test folders.
    """
    for split_type in split_ids:
        path = pathlib.Path(output_dir, split_type)
        os.makedirs(path, exist_ok=True)

    # reshuffle train and test images
    target_locs = {}
    for split_type in split_ids:
        target_locs[split_type] = []

        for source in split_ids[split_type]:
            target = pathlib.Path(
                output_dir, split_type, os.path.basename(source)
            ).resolve()
            copyfile(source, target)
            target_locs[split_type].append(target)

    # return paths in a dataframe
    split_df = []
    for k in target_locs.keys():
        for path in target_locs[k]:
            split_df.append({"split": k, "path": path})
    return pd.DataFrame(split_df)


class CellDataset(Dataset):
    """
    Dataset for working with tiffs of cells
    """
    def __init__(self, img_paths, xy_path=None):
        """Initialize dataset."""
        self.img_paths = img_paths

        # default xy values
        if xy_path:
            self.xy = pd.read_csv(xy_path, index_col="path")
        else:
            self.xy = {"y": np.zeros(len(img_paths))}

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, i):
        img = np.load(self.img_paths[i])
        y = self.xy.loc[self.img_paths[i], "y"]
        return torch.Tensor(img.transpose(2, 0, 1)), torch.Tensor([y])
