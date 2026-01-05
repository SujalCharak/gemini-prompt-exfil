# AIXT — RAG Exfiltration Probe

## Overview

This directory contains a focused security research probe conducted as part of **AIXT (AI eXposure & Trust)**.  
The objective of this probe was to evaluate whether **Retrieval-Augmented Generation (RAG)** pipelines could be abused to exfiltrate restricted or private data through model interaction, grounding, or retrieval logic.

Rather than targeting classical access-control bypasses, this work investigates **trust-boundary failures** in modern AI systems—where large language models rely on external data sources to ground their responses.

---

## Motivation

As RAG and embedding-based retrieval become foundational to enterprise AI systems, they introduce a new attack surface:

- External data connectors (e.g., document stores, drives)
- Retrieval and ranking layers
- LLM reasoning and response generation

Even when identity and permission controls are correct, **logical failures in how retrieved context is trusted, ranked, or presented** may lead to silent data exposure.

This probe was designed to answer a critical question:

> Can attacker-controlled inputs cause an LLM system to retrieve or surface private data through RAG pipelines without breaking traditional IAM controls?

---

## Scope & Safety

- All testing was performed using **accounts owned by the researcher**
- Only **synthetic test data** was used (no real PII or secrets)
- No attempts were made to bypass authentication, permissions, or safeguards
- The probe followed responsible disclosure principles and ethical testing practices

---

## High-Level Test Design

- A restricted document containing a high-entropy synthetic canary was used as the **victim artifact**
- Structured attacker-style queries were issued through a RAG-enabled pipeline
- Request metadata, timestamps, and model responses were captured
- Automated verification scanned all responses for:
  - exact canary matches
  - partial or verbatim leakage
- Backend sanity checks verified access controls via direct API calls

---

## Results

-  **No unauthorized retrieval observed**
-  **No private content or canary surfaced in model responses**
-  **Access controls enforced correctly** (HTTP 403 on direct fetch attempts)
-  **No VRP-grade vulnerability identified in this phase**

These results establish a **clean negative baseline** for RAG-based exfiltration attempts under this configuration.

---

## Why Negative Findings Matter

Negative results are a critical part of security research.

They demonstrate:
- Proper enforcement of IAM and connector permissions
- Hardening against naïve prompt-based or connector-based data leakage
- Maturity of current RAG access-control mechanisms

More importantly, these findings **informed a strategic pivot** in AIXT’s research direction.

---

## Research Pivot: From Access Control to Trust Boundaries

This probe confirmed that modern systems are increasingly resilient against direct data exfiltration attempts.

As a result, AIXT has shifted focus toward **deeper, systemic risks**, including:
- Embedding and context poisoning
- Retriever mis-ranking and relevance manipulation
- Index provenance and lifecycle security
- Over-trust between retrieval layers and LLM reasoning

These areas represent under-explored vulnerabilities where **logical failures**, rather than broken permissions, may lead to real-world impact.

---

## Contents of This Directory

- `headers_rag*.txt` — request metadata and timestamps
- `probe_log.csv` — consolidated probe execution log
- `queries.txt` — attacker-style test queries
- `response_rag*.json` — captured model responses
- `.gitignore` — ensures raw or sensitive artifacts are excluded

Sensitive victim artifacts (original files, hashes) are intentionally excluded and available only upon authorized request.

---

## Status

- **RAG probe:** completed
- **Outcome:** negative baseline established
- **Next phase:** embedding-level and retriever trust-boundary research (in progress)

---

## About AIXT

AIXT (AI eXposure & Trust) is a security research toolkit focused on identifying and closing trust gaps in modern AI systems.  
Its goal is to systematically analyze how LLMs interact with external data, where assumptions fail, and how to harden AI pipelines against both accidental and adversarial misuse.
