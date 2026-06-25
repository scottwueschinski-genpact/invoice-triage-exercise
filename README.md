# Invoice Exception Triage Agent: Build Exercise

Welcome, and thanks for making the time. This is a **hands-on, 60-minute build
exercise**. We are not testing trivia; we are watching how you *build* a small
agentic AI system with the tools you actually use day to day.

## The scenario

You are on the engineering team for a Genpact Accounts Payable shared-services
operation. Thousands of supplier invoices arrive every day. Most are clean and can
be paid automatically; the expensive work is the **exceptions**: invoices that do
not match their purchase order, come from an unknown or blocked vendor, are
duplicates, or were read badly by the extraction model.

Your job is to finish an **invoice exception triage agent**: it reads a raw invoice,
extracts the structured fields, checks them against the vendor master and purchase
orders using tools, applies the AP **policy guardrails**, and assigns each invoice
one of four actions (`auto_approve`, `hold`, `escalate`, or `reject`) with an
auditable reason.

Most of the system is already built. Four pieces are stubbed out and marked `TODO`.
You implement them.

## Ground rules

- **Use your AI coding assistant.** Claude Code, Codex, Cursor, Copilot, whatever you
  normally build with. Driving an AI well *is* the skill we are assessing. Think out
  loud and narrate what you are doing and why.
- **Verify your work.** Run `make test` and `make eval` as you go. We care a lot about
  whether you check what the AI produces rather than trusting it blindly.
- **It runs offline.** No API key and no internet are required. A deterministic mock
  LLM ships in the repo, so everything is reproducible.
- **Read the policy.** The rules you must enforce are in
  [`data/reference/policy.md`](data/reference/policy.md). Read it early.

## Setup (about 1 minute)

You only need **Python 3.10+**. There are no packages to install.

```bash
make setup     # confirms your Python version
make test      # run the test suite; it starts RED (failing). That is expected.
make eval      # run the agent over the invoice batch and score it
```

## Suggested 60 minutes

| Time | What |
|------|------|
| 0-5 min | Read this file, `TASK.md`, and `policy.md`. Run `make test` to see the failing suite. |
| 5-50 min | Implement the four TODOs (see `TASK.md`). Re-run `make test` / `make eval` constantly. |
| 50-60 min | Walk us through what you built, the trade-offs you made, and what you would do with more time. |

## What you are handed vs. what you build

- **Given:** data, schemas, the mock LLM provider, the vendor/PO lookup + 3-way match
  tools, the audit-record helper, the eval harness, and the agent's batch loop.
- **You build:** the four `TODO`s in `TASK.md`: extraction, the duplicate-check tool,
  the policy decision, and the per-invoice orchestration.

Start with `TASK.md`.
