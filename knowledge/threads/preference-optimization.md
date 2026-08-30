---
title: Preference optimization for LLM alignment
kind: thread
added: 2026-08-29
status: active
tags: [rlhf, alignment, preferences, post-training]
papers: [2023-dpo]
concepts: [kl-regularized-optimization]
---

# Preference optimization for LLM alignment

## The question this line is answering
Given pairs of "response A preferred over response B", how do we move a model
toward the preferred behaviour — cheaply, stably, and without over-optimizing a
proxy?

## Timeline / moves
- **RLHF / PPO** — reward model + on-policy RL on the KL-regularized objective.
  Works; unstable and heavy.
- **DPO (2023)** — [[2023-dpo]] — closed-form solution to the same objective;
  a classification loss on pairs, no reward model, no sampling. Big simplification.
- _(next: IPO, KTO, ORPO, online DPO — add as read)_

## Where it stands now
Direct methods are the default starting point. Open disagreements: whether
off-policy direct methods hit a ceiling that on-policy RL clears; how much
online/iterative data collection matters; robustness of `beta` selection.

## What I'd try
SFT → DPO baseline on a small model on the 5090, then measure the gap to a short
online-DPO or GRPO stage on the same preference budget.
