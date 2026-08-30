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

## Phase 2 — when you have 2-3 live projects
- **Quarto** installed system-wide (report.qmd already written; just `task report`)
- **pre-commit** running ruff + a metadata check
- **GitHub Actions**: run `task test` on push; `gh repo create` in `sconix new`
- **rclone or DVC** for `data/` and `models/` — pick DVC only if you need pipeline caching, else rclone to a cheap bucket
- second template: `paper-reproduction`

## Phase 3 — when experiment count outgrows `task compare`
- lightweight tracker: **aim** (local UI, no server) before MLflow
- **Docker / devcontainer** if a project needs a pinned CUDA userland
- **MkDocs Material** if notes outgrow flat markdown
- **Prefect** only if runs need scheduling + retries + monitoring

## Never (for a solo fast-moving researcher)
- Dagster, Airflow, n8n as core infra
- a bespoke plugin system
- more than ~4 templates
