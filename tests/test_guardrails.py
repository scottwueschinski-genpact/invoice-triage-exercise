import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent.guardrails import decide
from agent.schema import InvoiceExtraction, AUTO_APPROVE, HOLD, ESCALATE, REJECT

MATCHED = {"matched": True, "reason": "matched"}
NO_MATCH = {"matched": False, "reason": "po_mismatch"}
ACTIVE = {"vendor_id": "V1", "status": "active"}
BLOCKED = {"vendor_id": "V9", "status": "blocked"}


def _ext(total_amount=100.0, confidence=0.95):
    return InvoiceExtraction(
        invoice_number="X-1", vendor_name="Acme", invoice_date="2024-03-14",
        currency="USD", total_amount=total_amount, confidence=confidence, po_number="PO-1",
    )


class TestDecide(unittest.TestCase):
    def test_none_extraction_escalates(self):
        d = decide("i", None, None, None, False)
        self.assertEqual(d.action, ESCALATE)
        self.assertEqual(d.reason, "extraction_failed")

    def test_blocked_vendor_rejects(self):
        d = decide("i", _ext(), BLOCKED, MATCHED, False)
        self.assertEqual(d.action, REJECT)
        self.assertEqual(d.reason, "vendor_blocked")

    def test_duplicate_rejects(self):
        d = decide("i", _ext(), ACTIVE, MATCHED, True)
        self.assertEqual(d.action, REJECT)
        self.assertEqual(d.reason, "duplicate_invoice")

    def test_low_confidence_escalates(self):
        d = decide("i", _ext(confidence=0.60), ACTIVE, MATCHED, False)
        self.assertEqual(d.action, ESCALATE)
        self.assertEqual(d.reason, "low_confidence")

    def test_unknown_vendor_escalates(self):
        d = decide("i", _ext(), None, NO_MATCH, False)
        self.assertEqual(d.action, ESCALATE)
        self.assertEqual(d.reason, "unknown_vendor")

    def test_no_match_holds(self):
        d = decide("i", _ext(total_amount=1450.0), ACTIVE, NO_MATCH, False)
        self.assertEqual(d.action, HOLD)

    def test_over_threshold_escalates(self):
        d = decide("i", _ext(total_amount=12500.0), ACTIVE, MATCHED, False)
        self.assertEqual(d.action, ESCALATE)
        self.assertEqual(d.reason, "over_auto_approve_threshold")

    def test_clean_auto_approves(self):
        d = decide("i", _ext(total_amount=4800.0), ACTIVE, MATCHED, False)
        self.assertEqual(d.action, AUTO_APPROVE)
        self.assertEqual(d.reason, "clean_match_within_policy")


if __name__ == "__main__":
    unittest.main()
