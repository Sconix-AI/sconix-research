"""One consistent look for every figure you produce."""

from __future__ import annotations

from pathlib import Path


def use_style() -> None:
    import matplotlib as mpl

    mpl.rcParams.update(
        {
            "figure.figsize": (7, 4),
            "figure.dpi": 110,
            "savefig.dpi": 130,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.size": 11,
            "lines.linewidth": 1.8,
        }
    )


def plot_metric(run_dir: str | Path, y: str, x: str = "step", ax=None):
    """Quick line plot of a column in a run's metrics.jsonl."""
    import json

    import matplotlib.pyplot as plt

    use_style()
    rows = [
        json.loads(line)
        for line in (Path(run_dir) / "metrics.jsonl").read_text().splitlines()
        if line.strip()
    ]
    xs = [r.get(x) for r in rows if y in r]
    ys = [r[y] for r in rows if y in r]
    ax = ax or plt.gca()
    ax.plot(xs, ys, label=Path(run_dir).name)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    return ax


def save_fig(fig, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    return path
