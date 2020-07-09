"""
Utilities for working with multichannel Tiffs
"""
import torch
from torch.utils.data import Dataset
import pathlib
import rasterio
import numpy as np
import os

def tiff_to_numpy(input_path, output_path):
    imgf = rasterio.open(input_path)
    img = imgf.read().transpose(1, 2, 0)
    np.save(str(output_path), img)

def convert_dir_numpy(input_dir, output_dir):
    paths = list(pathlib.Path(input_dir).glob("*.tif"))

    for i, path in enumerate(paths):
        print(f"converting {path}\t{i}/{len(paths)}")
        out_name = pathlib.Path(path).stem + ".npy"
        tiff_to_numpy(path, pathlib.Path(output_dir, out_name))


class CellDataset(Dataset):
    """
    Dataset for working with tiffs of cells
    """

    def __init__(self, input_dir, transform=None):
        """Initialize dataset."""
        self.img_files = list(pathlib.Path(input_dir).glob("*npy"))
        self.transform = transform

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, i):
        img = np.load(self.img_files[i])
        if self.transform:
            img = self.transform(img)

        return torch.Tensor(img.transpose(2, 0, 1))



class RandomCrop(object):
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
    tiff_dir = pathlib.Path(os.environ["ROOT_DIR"], "data", "tiffs")
    npy_dir = pathlib.Path(os.environ["ROOT_DIR"], "data", "npys")
    convert_dir_numpy(tiff_dir, npy_dir)
    data = CellDataset(npy_dir, dt.RandomCrop(64))
    data[0]
