"""Policy guardrails and the triage decision. TODO 3 - see TASK.md and policy.md."""
from typing import Optional, Dict, Any
from .schema import Decision, InvoiceExtraction, AUTO_APPROVE, HOLD, ESCALATE, REJECT

# Policy thresholds (see data/reference/policy.md).
CONFIDENCE_FLOOR = 0.85
AUTO_APPROVE_THRESHOLD = 5000.0


def decide(
    invoice_id: str,
    extraction: Optional[InvoiceExtraction],
    vendor_record: Optional[Dict[str, Any]],
    match_result: Optional[Dict[str, Any]],
    is_duplicate: bool,
) -> Decision:
    """TODO 3 - return the triage Decision for one invoice.

    Enforce the policy in data/reference/policy.md. The rules are PRECEDENCE-ORDERED:
    the first matching rule wins. In summary:

      1. extraction is None ...................... escalate / extraction_failed
      2. vendor status == "blocked" ............... reject  / vendor_blocked
      3. is_duplicate ............................. reject  / duplicate_invoice
      4. confidence < CONFIDENCE_FLOOR ............ escalate / low_confidence
      5. vendor unknown (vendor_record is None) ... escalate / unknown_vendor
      6. no clean 3-way match ..................... hold    / (use match reason)
      7. amount > AUTO_APPROVE_THRESHOLD .......... escalate / over_auto_approve_threshold
      8. otherwise ................................ auto_approve / clean_match_within_policy

    Populate Decision.action, Decision.reason (use the reason codes above), and put
    whatever evidence you checked into Decision.checks so the decision is auditable.
    """
    raise NotImplementedError("TODO 3: implement the decision tree (see policy.md)")
