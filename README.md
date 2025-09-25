This repo publishes **sanitized** artifacts from our tests against modern multimodal LLMs.
Raw logs, keys, request IDs, and full leaks are excluded.
- **SYS suites** — Cases: **31** · BUG-LIKELY: **21**
- **HIA suites** — Cases: **32** · BUG-LIKELY: **15**

See `docs/METHODOLOGY.md` and `docs/DISCLOSURE.md`. Sanitized excerpts live in `sanitized_reports/`.
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
scripts/make_sanitized.sh
cat sanitized_reports/example_SANITIZED.json
