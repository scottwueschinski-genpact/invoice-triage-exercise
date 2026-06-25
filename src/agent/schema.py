"""Data models for the invoice triage agent. (GIVEN - you should not need to edit this.)"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

# --- Decision actions -------------------------------------------------------
AUTO_APPROVE = "auto_approve"
HOLD = "hold"
ESCALATE = "escalate"
REJECT = "reject"

VALID_ACTIONS = {AUTO_APPROVE, HOLD, ESCALATE, REJECT}


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    amount: float


@dataclass
class InvoiceExtraction:
    """The structured data an LLM extracts from a raw invoice."""
    invoice_number: str
    vendor_name: str
    invoice_date: str          # ISO date, e.g. "2024-03-14"
    currency: str
    total_amount: float
    confidence: float          # the model's self-reported confidence, 0.0 - 1.0
    po_number: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)


@dataclass
class Decision:
    """The triage outcome for one invoice."""
    invoice_id: str
    action: str                # one of VALID_ACTIONS
    reason: str                # a reason code, see data/reference/policy.md
    checks: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditRecord:
    """A full, auditable record of how one invoice was handled."""
    invoice_id: str
    decision: Decision
    extraction: Optional[InvoiceExtraction] = None
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
