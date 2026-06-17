# MNIST Non-Interactive ML Jobs Demo

Reusable Renku example showing how to run a non-interactive MNIST training job from a Zenodo data connector and launch a Streamlit inference dashboard. Python dependencies are specified in `pyproject.toml` for use with `uv`/standard Python packaging.

## Data

The training code expects the MNIST IDX files mounted from the Renku Zenodo data connector for DOI `10.5281/zenodo.10058130`, normally at:

```bash
/home/renku/work/mnist-dataset-doi-10.5281-zenodo.10058130
```

The code deliberately does **not** download MNIST at runtime. Set `MNIST_DATA_DIR` or pass `--data-dir` if the connector is mounted elsewhere.

## Training job

```bash
python -m mnist_jobs.train --data-dir /home/renku/work/mnist-dataset-doi-10.5281-zenodo.10058130 --model-dir /home/renku/work/models --target-accuracy 0.99
```

Training stops as soon as test accuracy reaches the target. Artifacts are written to a unique run directory so existing files are never overwritten.

## Dashboard

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8888
```

The dashboard loads the best available model from `MODEL_DIR`; if none is found, it can retrain a model using the mounted Zenodo connector data.
