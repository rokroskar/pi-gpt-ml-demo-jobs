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
model_dir = Path(os.getenv("MODEL_DIR", "/home/renku/work/models"))
target = float(os.getenv("TARGET_ACCURACY", "0.99"))

with st.sidebar:
    st.header("Configuration")
    st.write(f"Data: `{data_dir}`")
    st.write(f"Models: `{model_dir}`")
    st.write(f"Target accuracy: `{target}`")
    retrain = st.button("Retrain model", type="primary")

if retrain:
    with st.status("Training model...", expanded=True) as status:
        cmd = [sys.executable, "-m", "mnist_jobs.train", "--data-dir", str(data_dir), "--model-dir", str(model_dir), "--target-accuracy", str(target)]
        st.code(" ".join(cmd))
        proc = subprocess.run(cmd, text=True, capture_output=True)
        st.text(proc.stdout)
        if proc.returncode:
            st.error(proc.stderr)
            status.update(label="Training failed", state="error")
        else:
            status.update(label="Training complete", state="complete")

checkpoint = find_best_checkpoint(model_dir)
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
