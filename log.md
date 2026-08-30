# Research log

Newest on top (`sconix log "..."`). One line: what happened, what you learned.

- **2026-08-30** — sconix system: task run now auto-commits dirty changes before running (template v0.1.5 + vllm-explore) — no manual git commit needed for clean-sha run provenance
- **2026-08-30** — vllm-explore: first working vllm generation on RTX 5090 (WSL2) — fixed 3 env quirks (pin memory, stray system nvcc, CUDA13 subpackage skew), exp002 confirmed ~150 tok/s on facebook/opt-125m
- **2026-08-30** — vllm-explore: dropped stale cu128 torch index pin (template + project) — vllm needs CUDA13 libcudart, template now lets torch resolve its own wheel; template bumped to v0.1.4
- **2026-08-29** — lab live: OS + knowledge base pushed to 3 private GitHub repos (YusufRM); verified authorship = Yusuf only
- **2026-08-29** — built the OS; first project hello-5090 syncing torch
- **2026-08-29** — Sconix Research OS scaffolded: sconixlib + one project template + `sconix` CLI.
