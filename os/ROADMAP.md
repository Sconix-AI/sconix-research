# Roadmap — add only when a project demands it

The rule: a new tool enters the OS the day a real project makes its absence
hurt. Not before. Every addition is a template change + a `copier update` away
for existing projects.

## Phase 1 — now (done)
- uv, git/gh, ruff, pytest
- `sconixlib`: `Run`, `set_seed`, `get_device`/`gpu_info`, `load_config`, `load_runs`, `viz`
- one Copier template: research project with `experiments/`, `Run`-based reproducibility
- `sconix` CLI: new / ls / cap / log / compare / doctor
- Taskfile verbs: setup / run / exp / compare / report / lint / test

## Phase 2 — partly done (2026-08-29)
- [x] **Quarto** installed (`~/.local/quarto`, v1.6.40) — `task report` / `sconix report <proj>`
- [x] **pre-commit** in the template (`.pre-commit-config.yaml`, ruff + hygiene hooks) — `uv run pre-commit install`
- [x] **GitHub Actions** in the template (`.github/workflows/ci.yml`: ruff + pytest, CPU-only)
- [x] **`gh repo create`** wired into `sconix new` (private repo + push, unless `--no-gh`)
- [x] **JupyterLab** as a `notebook` dep group — `task lab`
- [ ] **rclone or DVC** for `data/` and `models/` — pick DVC only if you need pipeline caching, else rclone to a cheap bucket
- [ ] second template: `paper-reproduction` (extract it the 2nd time you clone a paper repo by hand)

## Phase 3 — when experiment count outgrows `task compare`
- lightweight tracker: **aim** (local UI, no server) before MLflow
- **Docker / devcontainer** if a project needs a pinned CUDA userland
- **MkDocs Material** if notes outgrow flat markdown
- **Prefect** only if runs need scheduling + retries + monitoring

## Never (for a solo fast-moving researcher)
- Dagster, Airflow, n8n as core infra
- a bespoke plugin system
- more than ~4 templates
