"""Read every run back as a table. No server, no database.

    from sconixlib import load_runs

    df = load_runs("results/*")          # one project
    df = load_runs("~/research/projects/*/results/*")   # everything
    print(df.sort_values("final_loss").head())
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _flatten(d: dict, prefix: str = "") -> dict:
    out: dict[str, Any] = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(_flatten(v, f"{key}."))
        else:
            out[key] = v
    return out


def load_runs(glob: str = "results/*"):
    """Return a DataFrame with one row per run dir that has a summary.json."""
    import pandas as pd

    glob = str(Path(glob).expanduser())
    base, _, pattern = glob.partition("*")
    rows = []
    for summ in Path(base or ".").glob("*" + pattern + "/summary.json"):
        try:
            data = json.loads(summ.read_text())
        except json.JSONDecodeError:
            continue
        row = _flatten(data)
        row["run_dir"] = str(summ.parent)
        rows.append(row)
    df = pd.DataFrame(rows)
    if "finished_at" in df:
        df = df.sort_values("finished_at", ascending=False).reset_index(drop=True)
    return df
