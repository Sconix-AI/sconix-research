# Sconix Research OS

A small engine that turns a question into a project, experiments, results, and a report — the same way every time, so the thinking is the only hard part.

## The loop

```
capture an idea      ->  sconix cap "what if attention heads specialise by ..."
turn it into a project ->  sconix new "head specialisation"
                           cd ~/research/projects/head-specialisation
                           task setup
frame + run experiments ->  task exp -- baseline
                           task run -- exp001_baseline
                           task compare
tell the story        ->  task report
```

## What's here

| Path | Purpose |
|---|---|
| `inbox.md` | 5-second idea capture. Triage weekly. |
| `log.md` | dated research log across all projects, newest on top |
| `os/sconixlib/` | the shared library every project installs (editable — improve it once, every project gets it) |
| `os/template/` | the single Copier template `sconix new` uses |
| `projects/` | generated projects live here |

## The two ideas that make this fast

1. **Every project is identical in shape.** Same `task` verbs, same folders, same `Run` wrapper. You never re-learn a project — and neither does an AI agent working in it.
2. **The engine is editable.** `sconixlib` is installed `--editable` into every project. Fix a bug or add a helper once in `os/sconixlib/`, and every project past and future picks it up.

## Commands

`sconix new | ls | cap | log | compare | doctor` — see `sconix help`.
Inside a project: `task setup | run | exp | compare | report | lint | test`.

## Deliberately not here yet

DVC, MLflow, Prefect, Dagster, n8n, MkDocs, a Typer CLI, 9 more templates.
Add each one only when a real project makes you feel its absence. See `os/ROADMAP.md`.
