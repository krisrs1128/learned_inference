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

    def __init__(self, input_dir):
        """Initialize dataset."""
        self.img_files = pathlib.Path(input_dir).glob("*npy")


if __name__ == '__main__':
    tiff_dir = pathlib.Path(os.environ["ROOT_DIR"], "data", "tiffs")
    npy_dir = pathlib.Path(os.environ["ROOT_DIR"], "data", "npys")
    convert_dir_numpy(tiff_dir, npy_dir)
