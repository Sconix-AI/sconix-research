"""GPU setup tuned for a single Blackwell card (RTX 5090)."""

from __future__ import annotations

from typing import Any


def get_device(prefer: str = "cuda") -> Any:
    """Return the best torch device and switch on fast matmul paths.

    On the 5090 this enables TF32 and high-precision bf16 matmuls, which is
    almost always what you want for research throughput.
    """
    import torch

    if prefer == "cuda" and torch.cuda.is_available():
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        try:
            torch.set_float32_matmul_precision("high")
        except Exception:
            pass
        return torch.device("cuda")
    return torch.device("cpu")


def gpu_info() -> dict:
    """Small dict describing the current CUDA device (safe to call without torch)."""
    try:
        import torch
    except ImportError:
        return {"torch": None}

    info: dict[str, Any] = {
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda": torch.version.cuda,
    }
    if torch.cuda.is_available():
        p = torch.cuda.get_device_properties(0)
        info.update(
            name=p.name,
            vram_gb=round(p.total_memory / 1024**3, 1),
            capability=f"{p.major}.{p.minor}",
            bf16=torch.cuda.is_bf16_supported(),
        )
    return info
