"""The Run context manager — the reproducibility spine of every experiment.

    from sconixlib import Run

    with Run("lr-sweep", config="configs/default.yaml", lr=3e-4) as run:
        model = build(run.cfg)
        for step, batch in enumerate(loader):
            loss = train_step(model, batch)
            run.log(step=step, loss=loss)
        run.summary(final_loss=loss, params=count_params(model))

What you get for free, written into ``results/<stamp>__<name>/``:

  * ``config.yaml``   — the fully resolved config (file + kwargs overrides)
  * ``env.json``      — git SHA + dirty flag, python/torch/CUDA, GPU, pip freeze
  * ``metrics.jsonl`` — one JSON object per ``run.log(...)`` call
  * ``summary.json``  — status, duration, your ``run.summary(...)`` values
  * ``console.log``   — everything printed during the run
  * figures via ``run.save_fig(fig, "name")``

``results/latest`` always points at the most recent run.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


def _git(*args: str, cwd: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return ""


class _Tee:
    """Mirror stdout/stderr into a file without hiding the terminal."""

    def __init__(self, stream, fh):
        self._stream = stream
        self._fh = fh

    def write(self, data):
        self._stream.write(data)
        try:
            self._fh.write(data)
        except ValueError:
            pass  # file closed mid-teardown

    def flush(self):
        self._stream.flush()
        try:
            self._fh.flush()
        except ValueError:
            pass

    def __getattr__(self, name):
        return getattr(self._stream, name)


class Run:
    def __init__(
        self,
        name: str,
        config: str | Path | dict | None = None,
        *,
        root: str | Path = "results",
        tags: list[str] | None = None,
        capture_console: bool | None = None,
        **overrides: Any,
    ):
        self.name = name
        self.tags = tags or []
        self.project_dir = Path.cwd()
        # Mirroring stdout into console.log is skipped under an outer test
        # harness that is already capturing output.
        if capture_console is None:
            capture_console = "PYTEST_CURRENT_TEST" not in os.environ
        self._capture_console = capture_console

        # ---- resolve config: file (if any) then kwargs overrides -------------
        cfg: dict[str, Any] = {}
        self.config_source = None
        if isinstance(config, dict):
            cfg = dict(config)
            self.config_source = "<dict>"
        elif config is not None:
            p = Path(config)
            if p.exists():
                cfg = yaml.safe_load(p.read_text()) or {}
                self.config_source = str(p)
        cfg.update(overrides)
        self.cfg = cfg

        # ---- run directory -------------------------------------------------
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        sha = _git("rev-parse", "--short", "HEAD", cwd=self.project_dir) or "nogit"
        self.dir = Path(root) / f"{stamp}__{name}__{sha}"
        self.dir.mkdir(parents=True, exist_ok=True)

        self._t0 = time.time()
        self._metrics_fh = (self.dir / "metrics.jsonl").open("w")
        self._console_fh = (self.dir / "console.log").open("w")
        self._summary: dict[str, Any] = {}
        self._git_sha = sha

    # -- lifecycle ---------------------------------------------------------
    def __enter__(self) -> Run:
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        if self._capture_console:
            sys.stdout = _Tee(self._old_stdout, self._console_fh)
            sys.stderr = _Tee(self._old_stderr, self._console_fh)

        (self.dir / "config.yaml").write_text(yaml.safe_dump(self.cfg, sort_keys=False))
        self._write_env()
        print(f"[sconix] run  {self.name}  ->  {self.dir}")
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        status = "ok" if exc_type is None else "failed"
        summary = {
            "name": self.name,
            "status": status,
            "tags": self.tags,
            "git_sha": self._git_sha,
            "duration_s": round(time.time() - self._t0, 2),
            "finished_at": datetime.now(UTC).isoformat(),
            "config": self.cfg,
            **self._summary,
        }
        if exc_type is not None:
            summary["error"] = "".join(traceback.format_exception(exc_type, exc, tb))
        (self.dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))

        if self._capture_console:
            sys.stdout = self._old_stdout
            sys.stderr = self._old_stderr
        self._metrics_fh.close()
        self._console_fh.close()

        latest = Path(self.dir.parent) / "latest"
        try:
            if latest.is_symlink() or latest.exists():
                latest.unlink()
            latest.symlink_to(self.dir.name)
        except OSError:
            (Path(self.dir.parent) / "LATEST.txt").write_text(self.dir.name)

        print(f"[sconix] {status}  {summary['duration_s']}s  ->  {self.dir}")
        return False  # never swallow exceptions

    # -- logging ---------------------------------------------------------
    def log(self, step: int | None = None, **metrics: Any) -> None:
        """Append one row of metrics to metrics.jsonl."""
        row = {"t": round(time.time() - self._t0, 3)}
        if step is not None:
            row["step"] = step
        row.update(metrics)
        self._metrics_fh.write(json.dumps(row, default=float) + "\n")
        self._metrics_fh.flush()

    def summary(self, **kv: Any) -> None:
        """Merge headline numbers into summary.json (call any time)."""
        self._summary.update(kv)

    def path(self, *parts: str) -> Path:
        """A path inside this run's directory (parents created)."""
        p = self.dir.joinpath(*parts)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def save_fig(self, fig, name: str, dpi: int = 130) -> Path:
        out = self.path("figures", f"{name}.png")
        fig.savefig(out, dpi=dpi, bbox_inches="tight")
        return out

    # -- internal ------------------------------------------------------
    def _write_env(self) -> None:
        from sconixlib.device import gpu_info

        try:
            freeze = subprocess.check_output(
                [sys.executable, "-m", "pip", "freeze"], text=True, stderr=subprocess.DEVNULL
            )
        except Exception:
            freeze = ""
        env = {
            "python": sys.version.split()[0],
            "argv": sys.argv,
            "config_source": self.config_source,
            "git_sha": _git("rev-parse", "HEAD", cwd=self.project_dir),
            "git_branch": _git("rev-parse", "--abbrev-ref", "HEAD", cwd=self.project_dir),
            "git_dirty": bool(_git("status", "--porcelain", cwd=self.project_dir)),
            "gpu": gpu_info(),
        }
        (self.dir / "env.json").write_text(json.dumps(env, indent=2, default=str))
        if freeze:
            (self.dir / "requirements.lock.txt").write_text(freeze)
        diff = _git("diff", cwd=self.project_dir)
        if diff:
            (self.dir / "git.diff").write_text(diff)
