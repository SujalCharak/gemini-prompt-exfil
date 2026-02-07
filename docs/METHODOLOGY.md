# Methodology

## Deterministic Runs
- Runs are seeded with `AIXT_SEED` (default 1337).
- `AIXT_RUN_ID` is a UTC timestamp for reproducible artifacts.

## Scenario-Driven Evaluation
- Scenarios define the inputs and adversarial setup.
- The harness executes scenarios and records traces.
- Validators assess model outputs and fail closed.

## Evidence-First Artifacts
- Every scenario emits a trace JSON artifact.
- Negative results are preserved and reported.

## Reporting
- Reports include summary verdicts and metadata.
- Negative results are included by default when requested.
