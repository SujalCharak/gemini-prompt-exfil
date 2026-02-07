# Threat Model

## Assets
- User-provided inputs (OCR, prompts, retrieved context).
- System prompts and policy scaffolding.
- Secrets provided to the runtime (tokens, API keys, credentials).
- Evaluation artifacts (traces, baselines, negative results).

## Adversaries
- Prompt injection attackers (direct and indirect).
- Retrieval poisoning via untrusted sources.
- Tool confusion attempts (misleading tool outputs or instructions).
- Insider misuse of privileged prompts or credentials.

## Trust Boundaries
- LLM adapters are untrusted data sources.
- Retrievers and tools are untrusted data sources.
- Validators and harness logic are trusted controls.

## Security Controls
- Deterministic execution with explicit seeds and run IDs.
- Trace artifacts for every evaluation.
- Fail-closed validators with structured evidence.
- Separation of scenario definition and evaluation logic.

## Out of Scope
- Real-time production monitoring.
- Human review workflows.
- Model-level safety training.
