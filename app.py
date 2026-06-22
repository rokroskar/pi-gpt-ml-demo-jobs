from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st
import torch

from mnist_jobs.artifacts import find_best_checkpoint, load_model
from mnist_jobs.data import sample_batch
from mnist_jobs.model import predict_proba

st.set_page_config(page_title="MNIST Renku Inference Demo", page_icon="✍️", layout="wide")
st.title("✍️ MNIST Renku Inference Demo")
st.caption("Uses MNIST mounted from the Zenodo data connector; no runtime data downloads.")

data_dir = Path(os.getenv("MNIST_DATA_DIR", "/home/renku/work/mnist-dataset-doi-10.5281-zenodo.10058130"))
# Prefer the public read-only Polybox mount for pre-trained models in the dashboard.
# Retraining writes to MODEL_WRITE_DIR, normally the writable Polybox mount.
model_read_dir = Path(os.getenv("MODEL_READ_DIR", "/home/renku/work/models-readonly"))
model_write_dir = Path(os.getenv("MODEL_WRITE_DIR", os.getenv("MODEL_DIR", "/home/renku/work/models")))
target = float(os.getenv("TARGET_ACCURACY", "0.99"))

with st.sidebar:
    st.header("Configuration")
    st.write(f"Data: `{data_dir}`")
    st.write(f"Read models: `{model_read_dir}`")
    st.write(f"Write models: `{model_write_dir}`")
    st.write(f"Target accuracy: `{target}`")
    retrain = st.button("Retrain model", type="primary")

if retrain:
    with st.status("Training model...", expanded=True) as status:
        cmd = [sys.executable, "-m", "mnist_jobs.train", "--data-dir", str(data_dir), "--model-dir", str(model_write_dir), "--target-accuracy", str(target)]
        st.code(" ".join(cmd))
        proc = subprocess.run(cmd, text=True, capture_output=True)
        st.text(proc.stdout)
        if proc.returncode:
            st.error(proc.stderr)
            status.update(label="Training failed", state="error")
        else:
            status.update(label="Training complete", state="complete")

checkpoints = [p for p in [find_best_checkpoint(model_read_dir), find_best_checkpoint(model_write_dir)] if p is not None]
checkpoint = None
if checkpoints:
    def _checkpoint_accuracy(path: Path) -> float:
        try:
            payload = torch.load(path, map_location="cpu")
            return float(payload.get("metrics", {}).get("accuracy", -1.0))
        except Exception:
            return -1.0

    checkpoint = max(checkpoints, key=_checkpoint_accuracy)

if checkpoint is None:
    st.warning("No trained model found. Use the sidebar button to train one from the mounted Zenodo connector.")
    st.stop()

model, payload = load_model(checkpoint)
metrics = payload.get("metrics", {})
st.success(f"Loaded `{checkpoint}` with test accuracy {metrics.get('accuracy', float('nan')):.5f}")

samples = sample_batch(data_dir, count=12)
images = torch.stack([x for x, _ in samples])
labels = [y for _, y in samples]
probs = predict_proba(model, images)
preds = probs.argmax(1).tolist()

cols = st.columns(4)
for i, (image, label, pred) in enumerate(zip(images, labels, preds)):
    with cols[i % 4]:
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        ax.imshow(image.squeeze(0), cmap="gray")
        ax.axis("off")
        st.pyplot(fig, clear_figure=True)
        ok = "✅" if pred == label else "❌"
        st.markdown(f"### {ok} prediction: `{pred}`")
        st.write(f"label: `{label}`, confidence: `{float(probs[i, pred]):.3f}`")
        st.bar_chart({str(k): float(v) for k, v in enumerate(probs[i])})
