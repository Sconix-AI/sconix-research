"""Merge layered YAML configs: defaults first, then per-experiment overrides."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(*paths: str | Path, **overrides: Any) -> dict:
    """Left-to-right merge of YAML files, then keyword overrides win.

    cfg = load_config("configs/default.yaml", "config.yaml", lr=1e-4)
    """
    cfg: dict[str, Any] = {}
    for p in paths:
        p = Path(p)
        if p.exists():
            cfg = _deep_merge(cfg, yaml.safe_load(p.read_text()) or {})
    return _deep_merge(cfg, overrides)
