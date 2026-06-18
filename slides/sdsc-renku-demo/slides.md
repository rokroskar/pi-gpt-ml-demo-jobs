---
theme: default
layout: cover
title: Pi + LLMs for Renku Experimentation
info: Agent-assisted data science workflows with Renku
footer: Pi + LLMs for Renku Experimentation
fonts:
  sans: Switzer
  serif: Switzer
  mono: 'Fira Code'
---

<img class="sdsc-cover-logo" src="./public/SDSC_logo_horizontal_rgb_white.png" alt="Swiss Data Science Center" />

# Pi + LLMs for Renku Experimentation

Agent-assisted data science workflows

<div class="sdsc-meta">Rok Roskar + Pi coding agent · 2026-06-18 · Renku MNIST jobs demo</div>

---
layout: section
---

<div class="sdsc-section-num">01</div>

# The idea

Use Pi and an LLM agent to turn a high-level data science request into a reproducible Renku project.

---

# The question

Can an LLM agent drive a full Renku experimentation workflow?

- write reusable code
- attach data connectors
- create launchers
- run jobs
- inspect logs
- document progress

<div class="sdsc-takeaway">MNIST is deliberately simple: the demo is about the workflow, not the dataset.</div>

---

# Agentic workflow

```text
User intent
   ↓
Pi + LLM agent
   ↓
Local code + Renku MCP tools
   ↓
Renku project
   ↓
Launchable experiments
```

---
layout: two-cols-header
---

# Why Renku + Pi?

::left::
## Renku provides

- projects
- data connectors
- launchers
- sessions
- non-interactive jobs
- reproducible environments

::right::
## Pi provides

- file editing
- shell execution
- MCP tool calls
- progress reporting
- human-in-the-loop control

---

# Initial prompt

> Create an example project on Renku that demonstrates how to run non-interactive ML training jobs.

> Use MNIST from Zenodo, train until accuracy is >0.99, and add a dashboard.

---

# What the agent planned

1. scaffold Python code
2. attach Zenodo MNIST data
3. create a Renku project
4. create a training launcher
5. run and monitor the job
6. add a Streamlit dashboard

---
layout: section
---

<div class="sdsc-section-num">02</div>

# Renku via MCP

The LLM did not click through the UI. It operated Renku through typed MCP tools.

---

# Renku MCP server

The Renku MCP server exposed operations for:

- projects and repositories
- data connectors
- launchers and environments
- builds and sessions
- non-interactive jobs
- logs and status

<div class="sdsc-takeaway">MCP turns Renku into an actionable API surface for the agent.</div>

---

# Example MCP tools

```text
renku_project_create
renku_connector_create
renku_project_repo_add
renku_launcher_create
renku_build_wait
renku_job_run
renku_session_logs
```

---
layout: section
---

<div class="sdsc-section-num">03</div>

# Demo implementation

A reusable ML project with Zenodo data, Polybox model storage, training jobs, and a dashboard.

---

# Repository structure

```text
src/mnist_jobs/
├── data.py        # MNIST IDX reader
├── model.py       # CNN model
├── train.py       # job entrypoint
└── artifacts.py   # checkpoints

app.py             # Streamlit dashboard
requirements.txt
scripts/
```

---

# Data rule

The training job must use mounted Renku data.

```text
MNIST DOI:
10.5281/zenodo.10058130
```

No ad-hoc downloads in training or dashboard code.

---
layout: two-cols-header
---

# Storage pattern

::left::
## Input data

Zenodo connector:

```text
/home/renku/work/
mnist-dataset-doi-...
```

Read-only and reproducible.

::right::
## Model artifacts

Polybox connectors:

- writable mount for jobs
- read-only mount for dashboard users
- timestamped output folders

---

# Training behavior

```bash
python -m mnist_jobs.train \
  --target-accuracy 0.99
```

- trains a PyTorch CNN
- evaluates after each epoch
- saves best checkpoints
- stops once target accuracy is reached

---

# Artifact safety

Runs write to unique folders:

```text
models/mnist-cnn-YYYYMMDDTHHMMSSZ/
├── model-epoch-XX-acc-*.pt
├── model-best.pt
├── metadata.json
└── summary.json
```

No overwrites of existing Polybox contents.

---
layout: section
---

<div class="sdsc-section-num">04</div>

# Results

The non-interactive job ran successfully on Renku and terminated early.

---

# Training result

<div class="sdsc-kpis">
  <div class="sdsc-kpi"><b>0.9907</b><span>final test accuracy</span></div>
  <div class="sdsc-kpi"><b>2</b><span>epochs to target</span></div>
  <div class="sdsc-kpi"><b>145 s</b><span>runtime on CPU</span></div>
</div>

<div class="sdsc-takeaway">The job wrote its best checkpoint to the writable Polybox connector and exited automatically.</div>

---

# Successful job log

```text
METRICS {"accuracy": 0.9853, "epoch": 1, ...}
Saved new best checkpoint: ...acc-0.98530.pt

METRICS {"accuracy": 0.9907, "epoch": 2, ...}
Saved new best checkpoint: ...acc-0.99070.pt

TARGET_REACHED accuracy=0.99070 target=0.99000
SUMMARY {"target_reached": true, ...}
```

---

# Dashboard

The dashboard launcher uses the built training image and runs Streamlit.

- shows MNIST samples
- loads the best model
- displays predictions
- can retrain if no checkpoint exists

---

# Streamlit in Renku sessions

Renku sets session URL variables at runtime.

```bash
streamlit run app.py \
  --server.address "$RENKU_SESSION_IP" \
  --server.port "$RENKU_SESSION_PORT" \
  --server.baseUrlPath "$RENKU_BASE_URL_PATH"
```

---
layout: section
---

<div class="sdsc-section-num">05</div>

# Human in the loop

The workflow was agent-assisted, not fully autonomous.

---

# User interventions

The user corrected the agent at several points:

- stop doing git operations
- test before claiming success
- use `requirements.txt`, not `uv`
- avoid launcher proliferation
- use Renku app-server env vars

---

# Lessons learned

- Make the agent report progress and blockers.
- Keep sensitive operations human-controlled.
- Use Renku connectors for data provenance.
- Prefer build-from-code for reusable environments.
- Treat platform failures as part of the experiment loop.

---

# What this demonstrates

Pi + LLM can orchestrate:

- code creation
- Renku setup through MCP
- data and model connectors
- launchers and jobs
- log-driven debugging
- documentation and slides

---

# Key takeaway

> The LLM is not replacing the data scientist.
>
> It is an execution assistant that turns intent into reproducible platform actions.

---
layout: cover
---

<img class="sdsc-cover-logo" src="./public/SDSC_logo_horizontal_rgb_white.png" alt="Swiss Data Science Center" />

# Questions?

<div class="sdsc-contact">
  <div>Rok Roskar</div>
  <div>Swiss Data Science Center</div>
  <div>datascience.ch</div>
</div>

<div class="sdsc-partners">
  <img src="./public/partners/ETH_Zurich_logo_white.png" alt="ETH Zürich" />
  <img src="./public/partners/EPFL_logo_white.png" alt="EPFL" />
  <img src="./public/partners/PSI_logo_white.png" alt="PSI" />
</div>
