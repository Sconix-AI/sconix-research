# Research log

Newest on top (`sconix log "..."`). One line: what happened, what you learned.

- **2026-08-30** — vllm-explore exp005: batch-size sweep {1..1024} on Qwen2.5-7B. Aggregate decode tok/s scales ~linearly to batch 64, knee at 128-256, saturates ~12,500 out tok/s. Per-request rate holds ~85 tok/s to batch 64 then collapses (45/24/12 at 256/512/1024). Serving sweet spot batch 64-128.
- **2026-08-30** — vllm-explore exp004: Qwen2.5-7B-Instruct batched decode = ~5,560 out tok/s @ batch 64 on the 5090 (43 req/s), reproducible. Cold start 111s (torch.compile+cudagraph+flashinfer autotune), warm 21s. Working set ~17GB. TTFT unavailable on vLLM 0.28 V1.
- **2026-08-30** — vllm-explore: Qwen2.5-7B-Instruct pulled + sha256-verified into $HF_HOME (15G). hf 1.29 has NO cross-run download resume (truncates fresh temp per run) — salvaged a 50% partial with ranged curl into blobs/. HF_TOKEN now OS-level via ~/.bashrc reading $HF_HOME/token.
- **2026-08-30** — sconix system: task run now auto-commits dirty changes before running (template v0.1.5 + vllm-explore) — no manual git commit needed for clean-sha run provenance
- **2026-08-30** — vllm-explore: first working vllm generation on RTX 5090 (WSL2) — fixed 3 env quirks (pin memory, stray system nvcc, CUDA13 subpackage skew), exp002 confirmed ~150 tok/s on facebook/opt-125m
- **2026-08-30** — vllm-explore: dropped stale cu128 torch index pin (template + project) — vllm needs CUDA13 libcudart, template now lets torch resolve its own wheel; template bumped to v0.1.4
- **2026-08-29** — lab live: OS + knowledge base pushed to 3 private GitHub repos (YusufRM); verified authorship = Yusuf only
- **2026-08-29** — built the OS; first project hello-5090 syncing torch
- **2026-08-29** — Sconix Research OS scaffolded: sconixlib + one project template + `sconix` CLI.
