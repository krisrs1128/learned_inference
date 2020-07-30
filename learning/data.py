"""
Utilities for working with multichannel Tiffs

python3 -m data
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


def parse_env(D):
    data_dir = pathlib.Path(os.environ["DATA_DIR"])
    for k, v in D.items():
        D[k] = data_dir / pathlib.Path(v)
    return D


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
    paths = list(pathlib.Path(input_dir).glob("*.tif"))
    for i, path in enumerate(paths):
        print(f"converting {path}\t{i}/{len(paths)}")
        out_name = pathlib.Path(path).stem + ".npy"
        tiff_to_numpy(path, pathlib.Path(output_dir, out_name))


def save_pngs(input_dir, output_dir):
    """
    Save arrays as pngs, for easier viewing
    """
    paths = list(pathlib.Path(input_dir).glob("*.npy"))
    for i, path in enumerate(paths):
        print(f"converting {path}\t{i}/{len(paths)}")
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

    target_locs = {}
    for split_type in split_ids:
        n_ids = len(split_ids[split_type])
        for i in range(n_ids):
            print(f"shuffling image {i}")
            source = split_ids[split_type][i]
            target = pathlib.Path(
                output_dir, split_type, os.path.basename(source)
            ).resolve()
            copyfile(source, target)
            target_locs[split_type].append(target)

    return target_locs



class CellDataset(Dataset):
    """
    Dataset for working with tiffs of cells
    """

    def __init__(self, input_dir, xy_path=None, transform=None, boot=None):
        """Initialize dataset."""
        self.img_files = list(pathlib.Path(input_dir).glob("*npy"))
        img_ids = [str(s) for s in self.img_files]
        img_ids = [re.search("[0-9]+", s).group() for s in img_ids]
        self.img_ids = [int(s) for s in img_ids]

        # default xy and bootstrap paths
        if xy_path:
            self.xy = pd.read_csv(xy_path)
        else:
            self.xy = {"y": np.zeros(len(img_ids))}

        if boot:
            self.resample_ix = boot
        else:
            self.resample_ix = np.arange(len(img_ids))

        # transforms, like crops and rotations
        self.transform = transform

    def __len__(self):
        import pdb
        pdb.set_trace()
        return len(self.img_ids)

    def __getitem__(self, i):
        ix = self.resample_ix[i]
        import pdb
        pdb.set_trace()
        img = np.load(self.img_ids[ix])
        y = self.xy["y"][self.img_ids[ix] - 1]

        if self.transform:
            img = self.transform(img)

        return torch.Tensor(img.transpose(2, 0, 1)), torch.Tensor([y]), [str(self.img_ids[ix])]


class RandomCrop():
    """Crop randomly the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """
    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, x):
        h, w = x.shape[:2]
        new_h, new_w = self.output_size

        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, w - new_w)
        return x[top: top + new_h, left: left + new_w]


if __name__ == '__main__':
    data_dir = pathlib.Path(os.environ["ROOT_DIR"], "data")
    convert_dir_numpy(data_dir / "tiffs", data_dir / "npys")
    save_pngs(data_dir / "npys", data_dir / "pngs")
    paths = list((data_dir / "npys").glob("*.npy"))
    splits = random_split(paths, [0.8, .1, .1])
    reshuffle(splits, data_dir)
