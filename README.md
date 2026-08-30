# Sconix Research OS

A small engine that turns a question into a project, experiments, results, and a report — the same way every time, so the thinking is the only hard part.

## The loop

```
read a paper         ->  sconix paper https://arxiv.org/abs/2305.18290
                         # place it on 5 facets, note what it changes for you
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
| `knowledge/` | the map — papers/concepts/threads placed on a faceted taxonomy (`knowledge/README.md`) |
| `os/sconixlib/` | the shared library every project installs (editable — improve it once, every project gets it) |
| `os/template/` | the single Copier template `sconix new` uses |
| `projects/` | generated projects live here |

## The two ideas that make this fast

1. **Every project is identical in shape.** Same `task` verbs, same folders, same `Run` wrapper. You never re-learn a project — and neither does an AI agent working in it.
2. **The engine is editable.** `sconixlib` is installed `--editable` into every project. Fix a bug or add a helper once in `os/sconixlib/`, and every project past and future picks it up.

## Commands

`sconix new | ls | cap | log | compare | report | sync | doctor` — see `sconix help`.
Knowledge: `sconix paper | concept | thread | kindex | kfind`.
Inside a project: `task setup | run | exp | compare | report | lab | lint | test`.

## Deliberately not here yet

DVC, MLflow, Prefect, Dagster, n8n, MkDocs, a Typer CLI, 9 more templates.
Add each one only when a real project makes you feel its absence. See `os/ROADMAP.md`.
