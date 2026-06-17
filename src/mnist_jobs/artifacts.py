from __future__ import annotations

from pathlib import Path

import torch

from .model import SmallMNISTCNN


def find_best_checkpoint(model_dir: str | Path) -> Path | None:
    root = Path(model_dir)
    if not root.exists():
        return None
    candidates = list(root.rglob("*.pt"))
    best_path = None
    best_acc = -1.0
    for path in candidates:
        try:
            payload = torch.load(path, map_location="cpu")
            acc = float(payload.get("metrics", {}).get("accuracy", -1))
        except Exception:
            continue
        if acc > best_acc:
            best_acc = acc
            best_path = path
    return best_path


def load_model(checkpoint: str | Path):
    payload = torch.load(checkpoint, map_location="cpu")
    model = SmallMNISTCNN()
    model.load_state_dict(payload["model_state_dict"])
    model.eval()
    return model, payload
