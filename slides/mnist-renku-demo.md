---
title: "Pi + LLMs for Renku Experimentation"
subtitle: "Agent-assisted data science workflows"
author: "Rok Roskar + Pi coding agent"
date: "2026-06-17"
revealOptions:
  transition: slide
  slideNumber: true
  hash: true
---

# Pi + LLMs for Renku Experimentation

### Agent-assisted data science workflows

MNIST training jobs on Renku as a concrete demo

---

## The question

Can an LLM agent help drive a full Renku data science workflow?

- code
- data connectors
- launchers
- jobs
- dashboards
- documentation

Note: The focus is not MNIST. MNIST is the test case.

---

## The workflow

```text
User intent
   ↓
Pi + LLM agent
   ↓
Local code + Renku API
   ↓
Reusable project
   ↓
Launchable experiments
```

---

## Why Renku?

Renku gives the agent concrete building blocks:

- projects
- repositories
- data connectors
- environments
- launchers
- jobs
- sessions

---

## Why Pi?

Pi gives the LLM safe tools to act:

- read/edit files
- run commands
- inspect status
- call MCP tools
- document progress

The agent can do more than suggest commands.

---

## Renku MCP server

Renku was driven through an MCP server.

The LLM used typed tools for:

- projects
- data connectors
- launchers
- builds and jobs

---

## Example MCP tools

```text
renku_project_create
renku_connector_create
renku_launcher_create
renku_build_wait
renku_job_run
```

MCP makes Renku actionable for the agent.

---

## Initial prompt

> Create an example project on Renku for non-interactive ML training jobs.

> Use MNIST from Zenodo, create launchers, train until accuracy is >0.99, and add a dashboard.

---

## User goal

Build a reusable Renku demo that:

- trains MNIST non-interactively
- uses Zenodo data
- stops at >99% accuracy
- exposes a dashboard
- is launchable with one click

---

## Agent plan

1. Write reusable Python code
2. Attach Zenodo MNIST data
3. Create Renku project
4. Create training launcher
5. Build image
6. Run job
7. Iterate
8. Add dashboard launcher

---

## Code generated

```text
src/mnist_jobs/
├── data.py       # MNIST IDX loader
├── model.py      # CNN
├── train.py      # job entrypoint
└── artifacts.py  # checkpoints

app.py            # Streamlit dashboard
requirements.txt
scripts/
```

---

## Data rule

The job must use Renku-mounted data.

```text
Zenodo DOI:
10.5281/zenodo.10058130
```

No ad-hoc downloads in training code.

---

## Training command

```bash
python -m mnist_jobs.train \
  --target-accuracy 0.99
```

The defaults point to the Renku Zenodo mount.

---

## Training behavior

- train CNN
- evaluate each epoch
- save best checkpoint
- stop once accuracy ≥ 0.99
- fail if target not reached

---

## Artifact safety

Artifacts go into unique run folders:

```text
models/mnist-cnn-<timestamp>/
```

No overwriting existing model files.

---

## Dashboard

Streamlit app for:

- loading best model
- showing MNIST samples
- displaying predictions
- retraining if model is missing

---

## Renku project created

```text
rokroskar/mnist-non-interactive-ml-jobs-demo
```

Repository:

```text
github.com/rokroskar/pi-gpt-ml-demo-jobs
```

---

## Data connector created

```text
Zenodo MNIST
DOI: 10.5281/zenodo.10058130
```

Mounted in Renku at:

```text
/home/renku/work/mnist-dataset-...
```

---

## Launcher created

```text
Train MNIST to 99% accuracy
```

- build from code
- Python builder
- ttyd frontend
- non-interactive job
- large resource class

---

## Current status

Training image build is running.

Next:

1. run job
2. inspect logs
3. check accuracy
4. iterate if needed
5. create dashboard launcher

---

## Human intervention matters

The user corrected the agent several times:

- stop doing git operations
- test the code locally
- update `.gitignore`
- refocus the slides
- reduce slide text

This is the desired control loop.

---

## Git handoff

Agent hit sandbox limits around git.

User pushed manually.

Agent then attached the repo to Renku.

```text
origin → GitHub repo
```

---

## Testing lesson

Agent initially only syntax-checked.

User asked for real testing.

Local testing was blocked by package/network limits.

Validation moved to the Renku-built image.

---

## `.gitignore` fix

User asked to exclude agent/runtime files.

Added:

```text
.pi/
.venv/
models/
data/
```

---

## Documentation

Progress was logged to Logseq:

```text
#[[MNIST Non-Interactive ML Jobs Demo]]
```

Useful for long-running agent workflows.

---

## What this demonstrates

Pi + LLM can orchestrate:

- code creation
- Renku setup
- data provenance
- launchers
- jobs
- dashboards
- documentation

---

## Key takeaway

The LLM is not replacing the scientist.

It acts as an execution assistant.

The human keeps intent, judgment, and approval.

---

## Open questions

- How much autonomy is appropriate?
- Where should approvals happen?
- How should credentials be handled?
- How should experiment results be tracked?

---

# Demo

1. Open Renku project
2. Show connector
3. Show launcher
4. Run/check job
5. Open dashboard

