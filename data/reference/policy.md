# AP Invoice Triage Policy (Genpact Shared Services)

The triage agent assigns every invoice exactly one **action**. Apply the rules in the
order below. **The first rule that matches wins** (precedence matters).

| # | Condition | Action | Reason code |
|---|-----------|--------|-------------|
| 1 | Extraction could not produce valid structured data | `escalate` | `extraction_failed` |
| 2 | Vendor exists in the vendor master with status `blocked` | `reject` | `vendor_blocked` |
| 3 | Invoice is a duplicate of one already processed | `reject` | `duplicate_invoice` |
| 4 | Extraction confidence is below the confidence floor | `escalate` | `low_confidence` |
| 5 | Vendor is not found in the vendor master (unknown/new vendor) | `escalate` | `unknown_vendor` |
| 6 | No clean 3-way match (PO missing, wrong vendor, or amount off) | `hold` | `missing_po` / `po_mismatch` |
| 7 | Amount is over the auto-approve threshold (but otherwise clean) | `escalate` | `over_auto_approve_threshold` |
| 8 | Everything above passes | `auto_approve` | `clean_match_within_policy` |

## Thresholds and definitions

- **Confidence floor:** `0.85`. Below this, a human must review the extraction.
- **Auto-approve threshold:** `5000.00` USD. Invoices over this require manager approval (escalate).
- **Clean 3-way match** means **all** of: the invoice references a PO that exists, the
  PO's vendor matches the invoice vendor, the PO is `open`, and the PO amount matches the
  invoice total within tolerance.
- **Amount tolerance:** the larger of `2%` of the PO amount or `$5.00`.
- **Duplicate** means: the same invoice number has already been processed, OR the same
  vendor + same total amount appears within a 30-day window.

## Why these rules exist (the business reasoning)

- **Never auto-approve a new/unknown vendor**, even for a small, clean-looking amount.
  Unvetted vendors are the classic vector for invoice fraud and must go through onboarding.
- **Never auto-approve below the confidence floor.** A low-confidence extraction means the
  agent is not sure what it read; paying on bad data is worse than a human review.
- **Duplicates are rejected, not paid twice.** Resubmissions are common and must be caught.
- **Every decision must carry a reason** so an auditor can reconstruct why money moved
  (or did not). Auditability is a hard requirement, not a nice-to-have.
