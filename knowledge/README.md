# Knowledge base

Where what you read fits in the larger system. Not folders — **coordinates**.

Every paper is stored once and placed on five independent axes
(`object`, `intervention_locus`, `mechanism`, `effect`, `evidence`) plus typed
relations to other notes. The controlled vocabularies are in
[`TAXONOMY.md`](TAXONOMY.md) — you classify by picking from lists, not inventing.

## Layout

| Path | What |
|---|---|
| `papers/` | one note per paper — YAML frontmatter (facets + relations) + a fixed prose template |
| `concepts/` | evergreen notes on ideas many papers touch (e.g. KL-regularized optimization) |
| `threads/` | your running synthesis of a research line — the story so far, in your words |
| `index.md` | **generated** by `sconix kindex`: papers under every facet value, the relation map, what still needs classifying |
| `TAXONOMY.md` | the five axes and their allowed values |
| `_templates/` | the note skeletons |

## Flow

```bash
# reading something
sconix paper https://arxiv.org/abs/2305.18290   # fetches title/authors/year
#   -> fill the frontmatter facets from TAXONOMY.md, write the prose sections
sconix kindex                                   # rebuild index.md

# later
sconix kfind "preference"                       # grep everything
sconix concept "reward hacking"                 # start a concept note
sconix thread  "long-context attention"         # start a thread
```

Capture-first is fine: `status: queued`, minimal frontmatter, prose stubbed.
`sconix kindex` lists anything missing `object` / `mechanism` / `effect` so
half-filed notes resurface instead of rotting.

## Why five axes and not one folder

"Training hack" is not a location. FlashAttention is
`(model, implementation.kernel, compute-allocation, efficiency, benchmark)` — an
attention *implementation*, not an attention *mechanism*. DPO and PPO-RLHF share
four of five coordinates and differ only in `intervention_locus`; the index puts
them next to each other and the `alternative_to` relation records the tension.
That adjacency is the "where does this fit" you're after.
