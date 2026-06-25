"""Audit-trail helpers. (GIVEN.)"""
from typing import Optional, Dict, Any
from .schema import AuditRecord, Decision, InvoiceExtraction


def build_audit_record(
    invoice_id: str,
    decision: Decision,
    extraction: Optional[InvoiceExtraction] = None,
    evidence: Optional[Dict[str, Any]] = None,
) -> AuditRecord:
    """Assemble an auditable record of how an invoice was handled."""
    return AuditRecord(
        invoice_id=invoice_id,
        decision=decision,
        extraction=extraction,
        evidence=evidence or {},
    )


def format_audit_record(record: AuditRecord) -> str:
    """One-line, human-readable summary for the console."""
    vendor = record.extraction.vendor_name if record.extraction else "(no extraction)"
    amount = f"{record.extraction.total_amount:,.2f}" if record.extraction else "n/a"
    return (
        f"{record.invoice_id:<8} {record.decision.action:<13} "
        f"{record.decision.reason:<28} {vendor:<26} {amount:>10}"
    )
