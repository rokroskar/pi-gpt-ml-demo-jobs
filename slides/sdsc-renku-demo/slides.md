---
theme: default
layout: cover
title: Pi + LLMs for Renku Experimentation
info: Agent-assisted project bootstrapping with Renku
footer: Pi + LLMs for Renku Experimentation
fonts:
  sans: Switzer
  serif: Switzer
  mono: 'Fira Code'
---

<img class="sdsc-cover-logo" :src="'/SDSC_logo_horizontal_rgb_white.png'" alt="Swiss Data Science Center" />

# Pi + LLMs for Renku Experimentation

<div class="renku-slogan"><span>Powered by Renku</span></div>

<div class="sdsc-meta">Rok Roškar + Pi coding agent · 2026-06-18 · Renku MNIST jobs demo</div>

---
layout: section
---

<div class="sdsc-section-num">01</div>

# The Question

Can an LLM agent help users get started with Renku faster?

---

# The bootstrapping problem

Renku gives users a lot of power:

- projects, repositories, environments
- data and storage connectors
- launchers, jobs, sessions, apps
- sharing and reproducibility patterns

<div class="sdsc-takeaway">For a new user, the challenge is often knowing which pieces to configure, and how they fit together.</div>

---

# Agent-assisted Renku setup

```text
User intent or existing repository
   ↓
Pi + LLM agent
   ↓
Renku context from MCP tools
   ↓
Configured project
   ↓
Launchable jobs and apps
   ↓
Logs and errors feed the next iteration
```

<div class="sdsc-takeaway">The agent acts as a guide through Renku concepts and configuration choices, then iterates on jobs and dashboards by inspecting logs.</div>

---
layout: two-cols-header
---

# What the agent brings

::left::
## LLM reasoning

- interprets a high-level goal
- plans project structure
- explains trade-offs
- adapts after failures

::right::
## Pi execution

- edits code and scripts
- runs local checks
- calls MCP tools
- keeps the user in control

---
layout: section
---

<div class="sdsc-section-num">02</div>

# Renku via MCP

The agent does not need to click through the UI. It interacts with Renku through typed tools and platform context.

---

# What is MCP?

MCP — the Model Context Protocol — is a standard way to connect LLM agents to external tools and context.

- tools expose typed actions the agent can call
- context explains how and when to use them
- authentication and permissions remain with the underlying service
- the agent can act without scraping UIs or inventing API calls

<div class="sdsc-takeaway">For Renku, MCP turns platform operations into structured capabilities an agent can reason about.</div>

---

# MCP server design goals

The Renku MCP server packages platform knowledge into tools the agent can safely call.

- command context: what each tool does, when to use it, and what to do next
- Renku knowledge: connectors, launchers, sessions, jobs, apps, and URL semantics
- OAuth handling: agents authenticate through the same Renku identity model as users
- API alignment: developed and tested against Renku APIs to avoid schema and behavior drift

<div class="sdsc-takeaway">Unlike a user-space skill or prompt file, a server-side MCP can be maintained by the platform team and updated as Renku evolves. <br>We expect live deployments such as <strong>renkulab.io</strong> to expose an MCP endpoint in the near future.</div>

---

# Platform knowledge matters

The agent can encode details that are easy to miss:

- which connector type to use when
- when to wait for a build before launching
- how to distinguish jobs, sessions, and apps
- how frontends must handle Renku session base paths

<div class="sdsc-takeaway">This is where an agent can reduce the configuration burden for new users.</div>

---

# Improving the tools through use

A second agent session was used to develop and refine the Renku MCP server itself.

```text
test agent struggles
   ↓
user reports issue
   ↓
MCP implementation improves
   ↓
future agents perform better
```

<div class="sdsc-takeaway">Real agent failures become better tool behavior, better docstrings, and better platform guidance.</div>

---
layout: section
---

<div class="sdsc-section-num">03</div>

# Demo project

A small MNIST workflow to demonstrate the pattern.

<div class="sdsc-takeaway"><a href="https://renku-ci-ui-4216.dev.renku.ch/p/rokroskar/mnist-non-interactive-ml-jobs-demo">Live project</a></div>

---

# Initial prompt

> Create an example project on Renku that demonstrates how to run non-interactive ML training jobs.
>
> Use MNIST from Zenodo, train until accuracy is above 99%, and add a dashboard.

<div class="sdsc-takeaway">The user gives intent; the agent works out the Renku resources and configuration steps.</div>

---

# What the demo creates

The agent bootstrapped a Renku project with:

- code for a PyTorch training job
- MNIST data from a Zenodo DOI connector
- model artifacts stored through Polybox
- a non-interactive training launcher
- a Streamlit inference dashboard

<div class="sdsc-takeaway">The same workflow could start from an existing repository instead of generated code.</div>

---

# The slides are part of the experiment

This deck was also created through the same agent-assisted process.

<div class="prompt-card">
  <div class="prompt-card-label">Simplified prompt</div>
  <div>Create a concise SDSC/Renku-branded presentation explaining the Pi + LLM + Renku demo workflow, focused on high-level concepts rather than implementation details.</div>
</div>

<div class="sdsc-takeaway">The experiment produced not only a Renku project, but also the communication material around it.</div>

---
layout: section
---

<div class="sdsc-section-num">04</div>

# What this shows

The interesting part is not MNIST — it is guided project onboarding.

---

# Key takeaways

- LLM agents can help translate intent into reproducible Renku actions.
- MCP gives the agent platform-specific context and safe tool boundaries.
- Human feedback remains essential for corrections and judgement.
- The same pattern can support generated code or existing repositories.

<div class="sdsc-takeaway">The agent helps users cross the gap from “I have code/data/a goal” to a configured Renku project.</div>

---

# The role of the agent

> The LLM is not replacing the data scientist.
>
> It is an execution assistant that helps turn intent into reproducible platform actions.

For Renku, that means connectors, environments, launchers, jobs, apps, and documentation — configured with the user in the loop.

---
layout: cover
---

<img class="sdsc-cover-logo" :src="'/SDSC_logo_horizontal_rgb_white.png'" alt="Swiss Data Science Center" />

# Questions?

<div class="sdsc-contact">
  <div>Rok Roškar</div>
  <div>Swiss Data Science Center</div>
  <div><a href="https://datascience.ch">datascience.ch</a></div>
  <div><a href="https://renkulab.io">renkulab.io</a></div>
</div>

<div class="sdsc-partners">
  <img :src="'/partners/ETH_Zurich_logo_white.png'" alt="ETH Zürich" />
  <img :src="'/partners/EPFL_logo_white.png'" alt="EPFL" />
  <img :src="'/partners/PSI_logo_white.png'" alt="PSI" />
</div>
