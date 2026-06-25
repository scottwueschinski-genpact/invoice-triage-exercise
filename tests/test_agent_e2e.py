import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent.agent import triage_batch
from agent.provider import MockProvider
from agent.schema import AUTO_APPROVE, HOLD, REJECT


def _load(name):
    with open(ROOT / name) as fh:
        return json.load(fh)


class TestAgentEndToEnd(unittest.TestCase):
    def setUp(self):
        invoices = _load("data/invoices.json")
        vendor_master = _load("data/reference/vendor_master.json")
        purchase_orders = _load("data/reference/purchase_orders.json")
        records = triage_batch(invoices, MockProvider(), vendor_master, purchase_orders)
        self.by_id = {r.invoice_id: r for r in records}

    def test_clean_invoice_auto_approves(self):
        self.assertEqual(self.by_id["inv_001"].decision.action, AUTO_APPROVE)

    def test_blocked_vendor_rejected(self):
        self.assertEqual(self.by_id["inv_005"].decision.action, REJECT)

    def test_po_mismatch_held(self):
        self.assertEqual(self.by_id["inv_011"].decision.action, HOLD)

    def test_missing_po_held(self):
        self.assertEqual(self.by_id["inv_012"].decision.action, HOLD)

    def test_every_record_has_a_reason(self):
        # Auditability: no decision may ship without a reason code.
        for record in self.by_id.values():
            self.assertTrue(record.decision.reason, f"{record.invoice_id} has no reason")


if __name__ == "__main__":
    unittest.main()
