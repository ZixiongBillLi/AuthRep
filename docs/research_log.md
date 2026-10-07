# Research Log

## 2026-10-07 — Pilot design and initial inference

### Dataset design

Highly sensitive actions such as credential access may introduce a separate safety-policy confound even when authorization is explicit.

Such cases should be reserved for later stress testing rather than the initial clean pilot set.

Role information is excluded from the initial authorization dataset and will instead be treated as a separate experimental variable.

### Initial inference setup

- Use Qwen3-4B as the pilot model.
- Run in BF16 rather than quantized format to avoid introducing quantization as a representation-level confound.
- Disable thinking mode for the initial experiments.
- Use the model's official chat template.
- Define the model response as only newly generated tokens; input prompt tokens are removed from `generate()` output before decoding.
- Start with deterministic generation for pipeline validation.

### Compute strategy

Develop and validate the experimental pipeline locally on a small open-weight model (approximately 3B–4B, preferably BF16).

Scale the main experiments to a 7B–8B model locally using memory-efficient inference if necessary.

Consider RIT Research Computing only if model size, dataset scale, or intervention experiments exceed local resources.

### Behavioral response format

Use unconstrained natural-language responses for the primary behavioral experiment.

Rationale:

Requiring the target model to emit a fixed `PROCEED` / `DO_NOT_PROCEED` flag may itself alter decision behavior by introducing a structured decision scaffold.

Behavioral labels will instead be derived post hoc from preserved raw responses.

Automated judging may be used later, but should:
- be validated against a manually labeled subset;
- classify response stance without relying on the ground-truth authorization condition.

### Generation length calibration

An initial run with a 512-token ceiling produced frequent truncation.

A calibration run using a 2048-token ceiling showed a maximum response length of 689 tokens across the 10 explicit-authorization prompts using Qwen3-4B.

Decision:

Use `max_new_tokens=1024` for the current explicit/Qwen3-4B dataset.

This value is not assumed globally; generation limits will be recalibrated for later datasets and models.

### Behavioral metrics and paired evaluation

The initial Qwen3-4B explicit-authorization pilot produced:

- `P(PROCEED | authorized) = 1.0`
- `P(PROCEED | unauthorized) = 0.0`
- `authorization_gap = 1.0`
- `expected_flip_rate = 1.0` across 5 matched scenarios

Aggregate proceed rates describe the overall behavioral tendency under each authorization condition, but they do not preserve which authorized and unauthorized responses belong to the same underlying scenario.

Because the dataset uses matched authorization pairs, pair-level analysis is also required. It measures whether changing only the authorization condition changes the model's behavior within the same scenario.

Pair-level outcomes can be classified as:

- `PROCEED → DO_NOT_PROCEED`: expected behavioral flip
- `DO_NOT_PROCEED → PROCEED`: reversed behavioral flip
- `PROCEED → PROCEED`: always proceed
- `DO_NOT_PROCEED → DO_NOT_PROCEED`: always refuse

Decision:
Use both aggregate authorization metrics and pair-level metrics in later experiments. Rename `pair_consistency` to `expected_flip_rate` because it more precisely describes the measured quantity.