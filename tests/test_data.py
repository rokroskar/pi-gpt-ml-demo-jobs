from __future__ import annotations

import gzip
import struct
from pathlib import Path

import numpy as np

from mnist_jobs.data import MNISTDataset, read_idx_images, read_idx_labels


def write_idx(root: Path):
    images = (np.arange(2 * 28 * 28, dtype=np.uint8) % 255).reshape(2, 28, 28)
    labels = np.array([3, 7], dtype=np.uint8)
    (root / "train-images-idx3-ubyte").write_bytes(struct.pack(">IIII", 2051, 2, 28, 28) + images.tobytes())
    with gzip.open(root / "train-labels-idx1-ubyte.gz", "wb") as f:
        f.write(struct.pack(">II", 2049, 2) + labels.tobytes())
    (root / "t10k-images-idx3-ubyte").write_bytes(struct.pack(">IIII", 2051, 2, 28, 28) + images.tobytes())
    (root / "t10k-labels-idx1-ubyte").write_bytes(struct.pack(">II", 2049, 2) + labels.tobytes())
    return images, labels


def test_idx_loader_reads_plain_and_gzip(tmp_path):
    images, labels = write_idx(tmp_path)
    assert read_idx_images(tmp_path / "train-images-idx3-ubyte").shape == images.shape
    assert read_idx_labels(tmp_path / "train-labels-idx1-ubyte.gz").tolist() == labels.tolist()
    ds = MNISTDataset(tmp_path, split="train")
    x, y = ds[1]
    assert x.shape == (1, 28, 28)
    assert y == 7
