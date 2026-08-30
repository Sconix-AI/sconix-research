---
title: KL-regularized policy optimization
kind: concept
added: 2026-08-29
object: [learning]
mechanism: [distribution-matching, gradient-shaping]
tags: [rlhf, regularization, kl, alignment]
see_also: [preference-optimization]
key_papers: [2023-dpo]
---

# KL-regularized policy optimization

## What it is
Optimize a policy to maximize reward **minus** `beta * KL(policy || reference)`.
The KL term anchors the new policy to a trusted reference (usually the SFT model),
so it improves on the reward signal without drifting into degenerate or
off-distribution behaviour. The KL-optimal policy has a closed form:
`pi*(y|x) proportional to pi_ref(y|x) * exp(reward(x,y) / beta)`.

## Why it matters
It is the shared backbone of modern alignment. RLHF/PPO optimizes it by sampling;
DPO solves it in closed form and fits the policy directly. `beta` is the single
knob trading reward-chasing against staying close to the reference.

## Variants / relatives
- **PPO-RLHF**: same objective, on-policy, explicit reward model.
- **DPO / IPO / KTO**: same objective, off-policy, reward folded into the loss.
- **Best-of-n / rejection sampling**: approximates the KL-optimal policy at
  inference instead of training.

## Papers that define or use it
- [[2023-dpo]]

## Open questions
- How does the right `beta` scale with model size and preference-data quality?
- When does the reference anchor help vs. cap achievable capability?
