"""One call to make a run reproducible."""

from __future__ import annotations

import os
import random


def set_seed(seed: int = 0, deterministic: bool = False) -> int:
    """Seed python, numpy, and torch (if installed).

    deterministic=True trades speed for bit-exact reproducibility.
    Returns the seed so callers can log it.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        if deterministic:
            torch.use_deterministic_algorithms(True, warn_only=True)
            torch.backends.cudnn.benchmark = False
            os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        else:
            torch.backends.cudnn.benchmark = True
    except ImportError:
        pass

    return seed
