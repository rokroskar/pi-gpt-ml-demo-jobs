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

<img class="sdsc-cover-logo" :src="'/SDSC_logo_horizontal_rgb_white.png'" alt="Swiss Data Science Center" />

# Pi + LLMs for Renku Experimentation

Agent-assisted data science workflows

<span class="renku-slogan">Connecting data, code, compute, and people.</span>

<div class="renku-co-brand"><span>Powered by Renku</span></div>

<div class="sdsc-meta">Rok Roskar + Pi coding agent · 2026-06-18 · Renku MNIST jobs demo</div>

---
layout: section
---

<div class="sdsc-section-num">01</div>

# The idea

Use Pi and an LLM agent to bootstrap a reproducible Renku project from a high-level request.

<div class="sdsc-takeaway">The agent helps navigate platform choices that are powerful but unfamiliar to new users.</div>

---

# The question

Can an LLM agent help a user get a Renku project off the ground?

- translate intent into project structure
- choose the right Renku resources
- configure data and storage connectors
- create launchers and environments
- run jobs and inspect logs
- document the workflow

<div class="sdsc-takeaway">MNIST is deliberately simple: the demo is about the workflow, not the dataset.</div>

---

# Agentic bootstrap workflow

```text
User intent or existing repository
   ↓
Pi + LLM agent
   ↓
Renku context from MCP tools
   ↓
Configured Renku project
   ↓
Launchable experiments and apps
```

<div class="sdsc-takeaway">The user does not need to know every connector, launcher, or app-server detail up front.</div>

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

This demo generated the code, but the same pattern applies when a user arrives with an existing repository.

---

# What the agent planned

1. scaffold or inspect the code repository
2. create a Renku project
3. attach Zenodo MNIST data
4. add Polybox model storage
5. create a training launcher
6. run and monitor the job
7. add a Streamlit dashboard app

---
layout: section
---

<div class="sdsc-section-num">02</div>

# Renku via MCP

The LLM did not click through the UI. It operated Renku through typed MCP tools.

<div class="renku-co-brand renku-co-brand-light"><span>Powered by Renku</span><img :src="'/renku-logo.svg'" alt="Renku" /></div>

---

# Renku MCP server

The Renku MCP server exposed operations for:

- projects and repositories
- data connectors
- launchers and environments
- builds and sessions
- non-interactive jobs
- logs and status

<div class="sdsc-takeaway">MCP turns Renku into an actionable API surface — and a source of platform context — for the agent.</div>

---

# What the agent learns from context

Through MCP and project state, the LLM can reason about Renku-specific choices:

- Zenodo DOI connectors for reproducible input data
- Polybox / SWITCHdrive connectors for model artifacts
- build-from-code versus external-image launchers
- non-interactive jobs versus interactive sessions
- Streamlit app path handling in Renku sessions

<div class="renku-callout">The agent is not guessing generic cloud commands; it is using Renku concepts exposed as typed tools.</div>

---

# Renku brings it together <img class="renku-logo-inline" :src="'/renku-logo.svg'" alt="Renku" />

<div class="renku-network" aria-label="Renku dot network showing data, code, compute, sessions and people">
  <div class="renku-node data">data</div>
  <div class="renku-node code">code</div>
  <div class="renku-node session">session</div>
  <div class="renku-node compute">compute</div>
  <div class="renku-node people">people</div>
</div>

<div class="renku-callout">Renku connects reusable research resources into one collaborative project space.</div>

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

# A second agent loop: improving MCP itself

In parallel, another agent session was building and refining the Renku MCP server.

- test agents exposed where the tools were confusing or incomplete
- user feedback was reported back to the MCP implementation agent
- tool docstrings and server instructions were updated with Renku-specific rules
- API edge cases became better tool behavior and better guidance

<div class="sdsc-takeaway">The MCP server is not static glue code — it improves through real agent failures.</div>

---

# Feedback that changed the tools

Examples from real test-agent runs:

- link connectors atomically when `project_id` is supplied
- wait for build-from-code environments before launching sessions
- filter stale hibernated sessions and scope lists by project
- check logs while waiting for jobs, not only session state
- use correct session URLs and Streamlit base-path semantics
- stop running sessions before deleting a project

<div class="renku-callout">This creates a feedback loop: agent struggles → user reports → MCP tools improve → future agents perform better.</div>

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

<div class="renku-callout">The dashboard turns a batch job artifact into something shareable with a team or community.</div>

---

# Streamlit in Renku sessions

The agent configured the app using Renku runtime variables instead of generic defaults.

```bash
streamlit run app.py \
  --server.address "$RENKU_SESSION_IP" \
  --server.port "$RENKU_SESSION_PORT" \
  --server.baseUrlPath "$RENKU_BASE_URL_PATH"
```

<div class="sdsc-takeaway">This is the kind of platform-specific detail that MCP context can make available to the LLM.</div>

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

- code creation or repository onboarding
- Renku setup through MCP
- data and model connectors
- launcher and app configuration
- log-driven debugging
- documentation and slides

<div class="sdsc-takeaway">The value is not only automation — it is guided project bootstrapping for users who are still learning Renku.</div>

---

# Key takeaway

> The LLM is not replacing the data scientist.
>
> It is an execution assistant that turns intent into reproducible platform actions.

For Renku, that means helping users cross the gap from “I have code/data/a goal” to a configured project with connectors, launchers, jobs, and apps.

---
layout: cover
---

<img class="sdsc-cover-logo" :src="'/SDSC_logo_horizontal_rgb_white.png'" alt="Swiss Data Science Center" />

# Questions?

<div class="sdsc-contact">
  <div>Rok Roskar</div>
  <div>Swiss Data Science Center</div>
  <div>datascience.ch</div>
</div>

<div class="sdsc-partners">
  <img :src="'/partners/ETH_Zurich_logo_white.png'" alt="ETH Zürich" />
  <img :src="'/partners/EPFL_logo_white.png'" alt="EPFL" />
  <img :src="'/partners/PSI_logo_white.png'" alt="PSI" />
</div>
