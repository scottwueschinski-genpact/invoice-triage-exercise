"""Agent orchestration. `triage_batch` is GIVEN; `triage_invoice` is TODO 4."""
from typing import List, Dict, Any
from .schema import AuditRecord, InvoiceExtraction
from .provider import LLMProvider
from .extract import extract_invoice
from .tools import vendor_lookup, po_lookup, three_way_match, duplicate_check
from .guardrails import decide
from .audit import build_audit_record


def triage_invoice(
    invoice: Dict[str, Any],
    provider: LLMProvider,
    vendor_master: Dict[str, Any],
    purchase_orders: Dict[str, Any],
    processed: List[InvoiceExtraction],
) -> AuditRecord:
    """TODO 4 - run one invoice end to end and return an AuditRecord.

    `invoice` is a dict with keys "invoice_id" and "raw_text".
    `processed` is the list of extractions already handled in this run (for dedup).

    Wire the pipeline together:
      1. extract_invoice(raw_text, provider)  -> may be None.
      2. If the extraction is None, decide(...) with extraction=None (escalate path).
      3. Otherwise gather evidence with the tools: vendor_lookup, po_lookup,
         three_way_match, and duplicate_check (against `processed`).
      4. Call decide(...) with that evidence to get the Decision.
      5. Return build_audit_record(...) carrying the decision, extraction, and evidence.

    Do NOT append to `processed` here - the caller does that.
    """
    raise NotImplementedError("TODO 4: wire the triage pipeline (see TASK.md)")


def triage_batch(
    invoices: List[Dict[str, Any]],
    provider: LLMProvider,
    vendor_master: Dict[str, Any],
    purchase_orders: Dict[str, Any],
) -> List[AuditRecord]:
    """Process a batch of invoices in order, accumulating processed extractions
    so duplicates can be detected. (GIVEN - relies on your triage_invoice.)"""
    processed: List[InvoiceExtraction] = []
    records: List[AuditRecord] = []
    for invoice in invoices:
        record = triage_invoice(invoice, provider, vendor_master, purchase_orders, processed)
        records.append(record)
        if record.extraction is not None:
            processed.append(record.extraction)
    return records
