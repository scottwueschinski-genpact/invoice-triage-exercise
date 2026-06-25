import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent.tools import duplicate_check
from agent.schema import InvoiceExtraction


def _ext(invoice_number, vendor_name, total_amount, invoice_date="2024-03-14"):
    return InvoiceExtraction(
        invoice_number=invoice_number,
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        currency="USD",
        total_amount=total_amount,
        confidence=0.95,
    )


class TestDuplicateCheck(unittest.TestCase):
    def test_empty_history_is_not_duplicate(self):
        self.assertFalse(duplicate_check(_ext("A-1", "Acme", 100.0), []))

    def test_same_invoice_number_is_duplicate(self):
        prior = [_ext("A-1", "Acme", 100.0)]
        self.assertTrue(duplicate_check(_ext("A-1", "Acme", 4800.0), prior))

    def test_same_vendor_amount_within_window_is_duplicate(self):
        prior = [_ext("A-1", "Acme", 100.0, "2024-03-14")]
        # different number, same vendor + amount, a few days later -> duplicate
        self.assertTrue(duplicate_check(_ext("A-2", "Acme", 100.0, "2024-03-20"), prior))

    def test_different_invoice_is_not_duplicate(self):
        prior = [_ext("A-1", "Acme", 100.0)]
        self.assertFalse(duplicate_check(_ext("B-9", "Brightline", 250.0), prior))


if __name__ == "__main__":
    unittest.main()
