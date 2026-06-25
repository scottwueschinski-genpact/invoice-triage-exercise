"""Tools the agent can call. (vendor_lookup / po_lookup / three_way_match are GIVEN.)

`duplicate_check` is TODO 2 - see TASK.md.
"""
from typing import Optional, List, Dict, Any
from .schema import InvoiceExtraction


def vendor_lookup(vendor_name: str, vendor_master: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the vendor master record for a vendor name, or None if unknown."""
    return vendor_master.get(vendor_name)


def po_lookup(po_number: Optional[str], purchase_orders: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the PO record for a PO number, or None if missing/unknown."""
    if not po_number:
        return None
    return purchase_orders.get(po_number)


def three_way_match(
    extraction: InvoiceExtraction,
    po_record: Optional[Dict[str, Any]],
    amount_tolerance_pct: float = 0.02,
    amount_tolerance_abs: float = 5.0,
) -> Dict[str, Any]:
    """Compare an invoice extraction against its PO record.

    Returns a dict with `matched` (bool) and a `reason` describing why, plus the
    component checks. A clean match requires: the PO exists, the PO vendor equals
    the invoice vendor, the PO is open, and the amounts agree within tolerance
    (the larger of `amount_tolerance_pct` of the PO amount or `amount_tolerance_abs`).
    """
    if po_record is None:
        return {"matched": False, "reason": "missing_po", "vendor_match": False, "amount_match": False}

    vendor_match = po_record.get("vendor_name") == extraction.vendor_name
    tolerance = max(po_record.get("amount", 0.0) * amount_tolerance_pct, amount_tolerance_abs)
    amount_match = abs(po_record.get("amount", 0.0) - extraction.total_amount) <= tolerance
    is_open = po_record.get("status") == "open"
    matched = vendor_match and amount_match and is_open

    if matched:
        reason = "matched"
    elif not vendor_match:
        reason = "vendor_mismatch"
    elif not amount_match:
        reason = "po_mismatch"
    else:
        reason = "po_not_open"

    return {
        "matched": matched,
        "reason": reason,
        "vendor_match": vendor_match,
        "amount_match": amount_match,
    }


def duplicate_check(extraction: InvoiceExtraction, processed: List[InvoiceExtraction]) -> bool:
    """TODO 2 - detect whether `extraction` duplicates one already in `processed`.

    Per data/reference/policy.md, an invoice is a duplicate if:
      - the same invoice number has already been processed, OR
      - the same vendor + same total amount appears within a 30-day window.

    `processed` is the list of InvoiceExtraction objects seen earlier in the run.
    Return True if this invoice is a duplicate, else False.
    """
    raise NotImplementedError("TODO 2: implement duplicate_check (see TASK.md and policy.md)")
