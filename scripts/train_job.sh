#!/usr/bin/env bash
set -euo pipefail
python -m mnist_jobs.train \
  --data-dir "${MNIST_DATA_DIR:-/home/renku/work/mnist-dataset-doi-10.5281-zenodo.10058130}" \
  --model-dir "${MODEL_DIR:-/home/renku/work/models}" \
  --target-accuracy "${TARGET_ACCURACY:-0.99}"
