# Taxonomy — the controlled vocabularies

Classification means **picking from these lists**, not inventing labels. Every
value below is a valid token for a paper's frontmatter. If nothing fits, use
`other` and add a free `tags:` entry — then, if it recurs, promote it here.

A paper is a point in this space:

    paper = (object, intervention_locus, mechanism, effect, evidence)

Five independent axes. Multi-value is fine and normal.

---

## 1. object — what is being studied

| token | meaning |
|---|---|
| `data` | the dataset itself: what's in it, how it's built |
| `representation` | learned features / embeddings / latent structure |
| `model` | the architecture and its components |
| `learning` | the training process — objectives, dynamics, procedures |
| `inference` | how a trained model is run / decoded / sampled |
| `evaluation` | how capability is measured; benchmarks, metrics, protocols |
| `deployment` | serving, monitoring, lifecycle in production |

## 2. intervention_locus — what part is changed (dotted = sub-part)

    architecture.{attention, memory, routing, normalization, positional, embedding, activation}
    objective.{loss, regularization, reward-model, auxiliary}
    optimization.{optimizer, lr-schedule, gradient, init, batching}
    data.{selection, filtering, augmentation, curriculum, synthesis, dedup, labeling}
    procedure.{pretraining, continued-pretraining, sft, preference-opt, rl, distillation}
    implementation.{kernel, precision, parallelism, quantization, kv-cache, compilation}
    adaptation.{full-ft, peft, lora, adapter, prompt, steering, merging}

Use the parent alone (`architecture`) if the sub-part doesn't matter.
"Training hack" is never a locus — say what it actually modifies.

## 3. mechanism — how the effect is produced

| token | the lever |
|---|---|
| `representation-shaping` | changes what features the model forms |
| `gradient-shaping` | changes the gradient signal (clipping, scaling, stop-grad) |
| `parameter-constraint` | limits/structures which parameters can move (LoRA, freezing) |
| `information-routing` | controls what information reaches where (attention, MoE, gating) |
| `credit-assignment` | changes how outcome signal is attributed to decisions (RL, TD) |
| `search-exploration` | adds search or exploration over outputs/policies |
| `distribution-matching` | pulls one distribution toward another (KD, DPO, flow matching) |
| `knowledge-transfer` | moves competence between models/tasks/modalities |
| `memory-modification` | adds/edits an explicit store (retrieval, KV, weights-as-memory) |
| `compute-allocation` | changes where FLOPs/params/time are spent (scaling, early-exit) |

## 4. effect — what it is meant to buy

`capability` · `alignment` · `generalization` · `robustness` · `efficiency` ·
`scalability` · `interpretability` · `safety` · `controllability` · `reliability`

## 5. evidence — how the claim is tested

`theory` · `controlled-experiment` · `ablation` · `benchmark` · `scaling-analysis` ·
`mechanistic-analysis` · `human-eval` · `production-eval` · `replication`

---

## Relations (in frontmatter)

Point to other notes by their filename stem (`papers/`, `concepts/`, `threads/`):

- `builds_on:` — this depends on / extends that
- `alternative_to:` — same goal, different route
- `contradicts:` — claims something incompatible
- `related:` — worth reading together
- `applied_in:` — experiments/projects that used it (`hello-5090/exp002_...`)

## Worked placements

| Thing | object | locus | mechanism | effect |
|---|---|---|---|---|
| Cross-entropy | learning | objective.loss | distribution-matching | capability |
| KL penalty (RLHF) | learning | objective.regularization | distribution-matching | alignment |
| Multi-head attention | model | architecture.attention | information-routing | capability |
| FlashAttention | model | implementation.kernel | compute-allocation | efficiency |
| Gradient clipping | learning | optimization.gradient | gradient-shaping | reliability |
| LR warmup | learning | optimization.lr-schedule | gradient-shaping | reliability |
| Mixed precision | learning | implementation.precision | compute-allocation | efficiency |
| LoRA | learning | adaptation.lora | parameter-constraint | efficiency |
| Data dedup | data | data.dedup | representation-shaping | generalization |
| DPO | learning | objective.reward-model, procedure.preference-opt | distribution-matching | alignment |
