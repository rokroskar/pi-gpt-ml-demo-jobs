from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader

from .data import MNISTDataset
from .model import SmallMNISTCNN


def parse_args():
    p = argparse.ArgumentParser(description="Train MNIST model from mounted Zenodo data.")
    p.add_argument("--data-dir", default=os.getenv("MNIST_DATA_DIR", "/home/renku/work/mnist-dataset-doi-10.5281-zenodo.10058130"))
    p.add_argument("--model-dir", default=os.getenv("MODEL_DIR", "/home/renku/work/models"))
    p.add_argument("--target-accuracy", type=float, default=float(os.getenv("TARGET_ACCURACY", "0.99")))
    p.add_argument("--epochs", type=int, default=int(os.getenv("EPOCHS", "12")))
    p.add_argument("--batch-size", type=int, default=int(os.getenv("BATCH_SIZE", "128")))
    p.add_argument("--learning-rate", type=float, default=float(os.getenv("LEARNING_RATE", "0.001")))
    p.add_argument("--seed", type=int, default=int(os.getenv("SEED", "7")))
    p.add_argument("--num-workers", type=int, default=int(os.getenv("NUM_WORKERS", "2")))
    p.add_argument("--allow-existing-model-dir", action="store_true", help="Reuse MODEL_DIR but still create a unique run subdirectory.")
    return p.parse_args()


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def unique_run_dir(model_dir: Path) -> Path:
    model_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = model_dir / f"mnist-cnn-{stamp}"
    candidate = base
    suffix = 1
    while candidate.exists():
        candidate = Path(f"{base}-{suffix}")
        suffix += 1
    candidate.mkdir(parents=False)
    return candidate


def evaluate(model, loader, device):
    model.eval()
    total = 0
    correct = 0
    loss_sum = 0.0
    criterion = nn.CrossEntropyLoss()
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            logits = model(images)
            loss = criterion(logits, labels)
            loss_sum += float(loss.item()) * labels.numel()
            correct += int((logits.argmax(1) == labels).sum().item())
            total += labels.numel()
    return {"loss": loss_sum / total, "accuracy": correct / total}


def save_checkpoint(run_dir: Path, model, metrics: dict, args, epoch: int):
    ckpt = run_dir / f"model-epoch-{epoch:02d}-acc-{metrics['accuracy']:.5f}.pt"
    if ckpt.exists():
        raise FileExistsError(f"Refusing to overwrite existing checkpoint {ckpt}")
    payload = {
        "model_state_dict": model.state_dict(),
        "metrics": metrics,
        "epoch": epoch,
        "model_class": "SmallMNISTCNN",
        "args": vars(args),
    }
    torch.save(payload, ckpt)
    metadata = run_dir / "metadata.json"
    metadata.write_text(json.dumps({
        "checkpoint": ckpt.name,
        "metrics": metrics,
        "epoch": epoch,
        "model_class": "SmallMNISTCNN",
        "args": vars(args),
    }, indent=2))
    return ckpt


def main():
    args = parse_args()
    set_seed(args.seed)
    data_dir = Path(args.data_dir)
    model_dir = Path(args.model_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory {data_dir} does not exist; mount the Zenodo connector first.")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device={device}")
    print(f"Reading MNIST from mounted data connector: {data_dir}")
    print(f"Writing artifacts below: {model_dir} (unique run subdirectory; no overwrites)")

    train_ds = MNISTDataset(data_dir, split="train", augment=True)
    test_ds = MNISTDataset(data_dir, split="test", augment=False)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers)
    test_loader = DataLoader(test_ds, batch_size=512, shuffle=False, num_workers=args.num_workers)

    run_dir = unique_run_dir(model_dir)
    model = SmallMNISTCNN().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(args.epochs, 1))
    criterion = nn.CrossEntropyLoss()
    best = {"accuracy": 0.0, "loss": float("inf")}
    best_ckpt = None
    start = time.time()

    for epoch in range(1, args.epochs + 1):
        model.train()
        running_loss = 0.0
        seen = 0
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            running_loss += float(loss.item()) * labels.numel()
            seen += labels.numel()
        scheduler.step()
        metrics = evaluate(model, test_loader, device)
        metrics.update({"epoch": epoch, "train_loss": running_loss / seen, "elapsed_seconds": round(time.time() - start, 2)})
        print("METRICS " + json.dumps(metrics, sort_keys=True), flush=True)
        if metrics["accuracy"] > best["accuracy"]:
            best = metrics
            best_ckpt = save_checkpoint(run_dir, model, metrics, args, epoch)
            print(f"Saved new best checkpoint: {best_ckpt}", flush=True)
        if metrics["accuracy"] >= args.target_accuracy:
            print(f"TARGET_REACHED accuracy={metrics['accuracy']:.5f} target={args.target_accuracy:.5f}; terminating early.", flush=True)
            break

    summary = {
        "target_accuracy": args.target_accuracy,
        "best_accuracy": best["accuracy"],
        "best_loss": best["loss"],
        "best_checkpoint": str(best_ckpt) if best_ckpt else None,
        "run_dir": str(run_dir),
        "target_reached": best["accuracy"] >= args.target_accuracy,
        "elapsed_seconds": round(time.time() - start, 2),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print("SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    if best_ckpt:
        # Convenience copy inside the unique run dir only; never touches pre-existing connector files.
        latest = run_dir / "model-best.pt"
        if not latest.exists():
            shutil.copy2(best_ckpt, latest)
    if not summary["target_reached"]:
        raise SystemExit(f"Target accuracy not reached: {best['accuracy']:.5f} < {args.target_accuracy:.5f}")


if __name__ == "__main__":
    main()
