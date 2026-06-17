from __future__ import annotations

import gzip
import struct
from pathlib import Path
from typing import Iterable

import numpy as np
import torch
from torch.utils.data import Dataset

IMAGE_FILES = {
    "train": ("train-images-idx3-ubyte", "train-images-idx3-ubyte.gz"),
    "test": ("t10k-images-idx3-ubyte", "t10k-images-idx3-ubyte.gz"),
}
LABEL_FILES = {
    "train": ("train-labels-idx1-ubyte", "train-labels-idx1-ubyte.gz"),
    "test": ("t10k-labels-idx1-ubyte", "t10k-labels-idx1-ubyte.gz"),
}


def _find_file(data_dir: Path, names: Iterable[str]) -> Path:
    for name in names:
        matches = list(data_dir.rglob(name))
        if matches:
            return matches[0]
    raise FileNotFoundError(
        f"Could not find any of {list(names)} below {data_dir}. "
        "Mount the Zenodo MNIST connector; runtime downloads are intentionally disabled."
    )


def _read_bytes(path: Path) -> bytes:
    if path.suffix == ".gz":
        with gzip.open(path, "rb") as f:
            return f.read()
    return path.read_bytes()


def read_idx_images(path: Path) -> np.ndarray:
    raw = _read_bytes(path)
    magic, n, rows, cols = struct.unpack(">IIII", raw[:16])
    if magic != 2051:
        raise ValueError(f"{path} is not an IDX image file (magic={magic})")
    arr = np.frombuffer(raw, dtype=np.uint8, offset=16)
    return arr.reshape(n, rows, cols)


def read_idx_labels(path: Path) -> np.ndarray:
    raw = _read_bytes(path)
    magic, n = struct.unpack(">II", raw[:8])
    if magic != 2049:
        raise ValueError(f"{path} is not an IDX label file (magic={magic})")
    arr = np.frombuffer(raw, dtype=np.uint8, offset=8)
    return arr.reshape(n)


class MNISTDataset(Dataset):
    def __init__(self, data_dir: str | Path, split: str = "train", augment: bool = False):
        if split not in {"train", "test"}:
            raise ValueError("split must be 'train' or 'test'")
        self.data_dir = Path(data_dir)
        image_path = _find_file(self.data_dir, IMAGE_FILES[split])
        label_path = _find_file(self.data_dir, LABEL_FILES[split])
        images = read_idx_images(image_path).astype("float32") / 255.0
        labels = read_idx_labels(label_path).astype("int64")
        if len(images) != len(labels):
            raise ValueError(f"image/label length mismatch: {len(images)} != {len(labels)}")
        self.images = images
        self.labels = labels
        self.augment = augment

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int):
        image = torch.from_numpy(self.images[idx]).unsqueeze(0)
        label = int(self.labels[idx])
        if self.augment:
            # Lightweight augmentation that helps exceed 99% on CPU while avoiding torchvision.
            if torch.rand(()) < 0.4:
                shift_y = int(torch.randint(-1, 2, ()).item())
                shift_x = int(torch.randint(-1, 2, ()).item())
                image = torch.roll(image, shifts=(shift_y, shift_x), dims=(1, 2))
        return image, label


def sample_batch(data_dir: str | Path, count: int = 12):
    ds = MNISTDataset(data_dir, split="test", augment=False)
    rng = np.random.default_rng(123)
    idxs = rng.choice(len(ds), size=min(count, len(ds)), replace=False)
    return [ds[int(i)] for i in idxs]
