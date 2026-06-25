import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent.extract import extract_invoice
from agent.provider import MockProvider
from agent.schema import InvoiceExtraction


def _invoices():
    with open(ROOT / "data" / "invoices.json") as fh:
        return {row["invoice_id"]: row["raw_text"] for row in json.load(fh)}


class TestExtract(unittest.TestCase):
    def setUp(self):
        self.provider = MockProvider()
        self.invoices = _invoices()

    def test_clean_invoice_parses(self):
        result = extract_invoice(self.invoices["inv_001"], self.provider)
        self.assertIsInstance(result, InvoiceExtraction)
        self.assertEqual(result.invoice_number, "AC-2024-3391")
        self.assertEqual(result.vendor_name, "Acme Industrial Supply")
        self.assertEqual(result.po_number, "PO-5001")
        self.assertAlmostEqual(result.total_amount, 4800.0)
        self.assertAlmostEqual(result.confidence, 0.97)
        self.assertEqual(len(result.line_items), 1)

    def test_handles_markdown_code_fences(self):
        # inv_007 comes back wrapped in ```json ... ``` - it must still parse.
        result = extract_invoice(self.invoices["inv_007"], self.provider)
        self.assertIsInstance(result, InvoiceExtraction)
        self.assertEqual(result.vendor_name, "Summit Facilities Mgmt")
        self.assertAlmostEqual(result.total_amount, 4950.0)

    def test_malformed_json_returns_none_not_crash(self):
        # inv_009 comes back as broken JSON - extract must fail safe (None).
        result = extract_invoice(self.invoices["inv_009"], self.provider)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
