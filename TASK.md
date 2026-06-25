# Your Tasks

Implement the four `TODO`s below. They are ordered, but you can work in any order.
Run `make test` and `make eval` continuously to check yourself. The unit tests
define the exact contracts; the policy is in `data/reference/policy.md`.

> Tip: the mock LLM behaves like a real one. It mostly returns clean JSON, but one
> invoice comes back wrapped in ```` ```json ```` fences, one comes back as broken
> JSON, and several report low confidence. Handle reality, not the happy path.

---

## TODO 1: Structured extraction (`src/agent/extract.py`)

Implement `extract_invoice(raw_text, provider)`:

1. Build the prompt (use the provided `EXTRACTION_PROMPT`) and call `provider.complete(...)`.
2. Parse the response into JSON. Strip markdown code fences if present.
3. Validate the required fields and types; build and return an `InvoiceExtraction`.
4. If you cannot get valid structured data, **return `None`**: do not crash and do
   not pass fabricated data downstream.

**Done when:** `tests/test_extract.py` passes (clean parse, fenced JSON, and the
malformed case returning `None`).

## TODO 2: Duplicate detection tool (`src/agent/tools.py`)

Implement `duplicate_check(extraction, processed)`. An invoice is a duplicate if the
same invoice number was already processed, **or** the same vendor + same total amount
appears within a 30-day window (see `policy.md`).

**Done when:** `tests/test_tools.py` passes.

## TODO 3: Policy guardrails and decision (`src/agent/guardrails.py`)

Implement `decide(...)`. Apply the **precedence-ordered** rules in `policy.md` and
return a `Decision` with the right `action`, the right `reason` code, and the checks
you ran in `Decision.checks` (for auditability). This is the heart of the exercise:
get the precedence and the "never auto-approve an unsafe invoice" rules right.

**Done when:** `tests/test_guardrails.py` passes.

## TODO 4: Wire the pipeline (`src/agent/agent.py`)

Implement `triage_invoice(...)`: extract, then gather evidence with the tools, then
`decide(...)`, then return an `AuditRecord`. Handle the `None`-extraction case.

**Done when:** `tests/test_agent_e2e.py` passes and `make eval` reports **PASS**
(at least 80% accuracy on the visible gold labels).

---

## Deliverables

1. A working repo: `make test` green and `make eval` reporting PASS.
2. A short **`DECISIONS.md`** (5 to 10 lines): the key choices and trade-offs you made,
   anything you did *not* trust the AI on, and what you would do with another hour.

## Bonus (only if you finish early)

- Wire `RealProvider` in `src/agent/provider.py` to a real model with your own key
  (stdlib `urllib`, see `.env.example`) and demo it live.
- Add structured logging/observability to the triage loop.
- Harden an edge case you noticed that the tests do not yet cover.

## How we will look at your work

We grade on a hidden set of additional cases (the same policy, new invoices), so
build for the *rules*, not for the visible tests. We are looking at: does it run and
pass; did you handle the messy LLM output; is the policy precedence correct
(especially the cases where an invoice looks fine but must not be auto-approved); is
the code clean; and how well you drove and verified your AI assistant throughout.
