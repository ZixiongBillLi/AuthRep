# AuthRep

## Research Question

Do safety-aligned language models encode authorization status in their internal representations, and does that representation causally influence behavioral compliance?

## Motivation

Behavioral compliance does not necessarily imply that a security constraint is robustly represented or causally used by a model.

This project studies one narrow security concept: authorization boundaries.

## Phase 1

1. Construct paired authorized / unauthorized scenarios.
2. Measure behavioral compliance.
3. Probe hidden representations for authorization information.
4. Test causal relevance using activation intervention.
5. Evaluate generalization on paraphrased and implicit authorization contexts.

## Scope

This project does not initially study autonomous agents, real-world exploitation, multi-agent coordination, or broad AI security.

## Status

Project initialized.

Observation: Highly sensitive actions such as credential access may introduce a separate safety-policy confound even when authorization is explicit. Keep such cases for later stress testing rather than the initial clean pilot set.