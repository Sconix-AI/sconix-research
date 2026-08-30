"""Sconix Research OS — shared primitives.

Import surface is deliberately tiny:

    from sconixlib import Run, set_seed, get_device, gpu_info, load_runs

Everything a run needs lives on the ``Run`` object.
"""

from sconixlib.config import load_config
from sconixlib.device import get_device, gpu_info
from sconixlib.run import Run
from sconixlib.seed import set_seed
from sconixlib.track import load_runs

__all__ = ["Run", "set_seed", "get_device", "gpu_info", "load_runs", "load_config"]
__version__ = "0.1.0"
