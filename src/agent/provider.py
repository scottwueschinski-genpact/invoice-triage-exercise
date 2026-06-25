"""LLM provider abstraction. (GIVEN.)

The default `MockProvider` is deterministic and runs fully offline, so the whole
system works with no API key and grading is reproducible. It mimics a real LLM:
mostly clean JSON, but with the kind of messy output you get in production
(one invoice comes back as broken JSON; one is wrapped in markdown code fences;
several report low confidence). Your extraction code has to cope with that.

`RealProvider` is an OPTIONAL bonus: wire a real model with your own key
(stdlib `urllib` only, no vendor SDK required). See `.env.example`.
"""
from typing import Protocol


class LLMProvider(Protocol):
    def complete(self, prompt: str) -> str:
        """Return the model's raw text response for a prompt."""
        ...


# --- Canned model outputs, keyed by the invoice id found in the prompt ------
# These are the *raw strings a model would emit* - parsing them is your job.
_MOCK_RESPONSES = {
    "inv_001": '{"invoice_number":"AC-2024-3391","vendor_name":"Acme Industrial Supply","invoice_date":"2024-03-14","currency":"USD","total_amount":4800.0,"confidence":0.97,"po_number":"PO-5001","line_items":[{"description":"Steel brackets","quantity":200,"unit_price":24.0,"amount":4800.0}]}',
    "inv_002": '{"invoice_number":"BR-2024-1180","vendor_name":"Brightline Office Co","invoice_date":"2024-03-15","currency":"USD","total_amount":320.0,"confidence":0.95,"po_number":"PO-5003","line_items":[{"description":"Copy paper (ream)","quantity":40,"unit_price":8.0,"amount":320.0}]}',
    "inv_003": '{"invoice_number":"AC-2024-3402","vendor_name":"Acme Industrial Supply","invoice_date":"2024-03-16","currency":"USD","total_amount":2100.0,"confidence":0.60,"po_number":"PO-5005","line_items":[{"description":"Hex bolts","quantity":1400,"unit_price":1.5,"amount":2100.0}]}',
    "inv_004": '{"invoice_number":"GL-2024-7781","vendor_name":"Global Logistics Partners","invoice_date":"2024-03-12","currency":"USD","total_amount":12500.0,"confidence":0.96,"po_number":"PO-5002","line_items":[{"description":"Q1 freight & distribution","quantity":1,"unit_price":12500.0,"amount":12500.0}]}',
    "inv_005": '{"invoice_number":"NW-2024-0455","vendor_name":"Northwind Traders","invoice_date":"2024-03-10","currency":"USD","total_amount":1500.0,"confidence":0.94,"po_number":null,"line_items":[{"description":"Miscellaneous supplies","quantity":1,"unit_price":1500.0,"amount":1500.0}]}',
    "inv_006": '{"invoice_number":"ZP-2024-2210","vendor_name":"Zenith Paper & Packaging","invoice_date":"2024-03-18","currency":"USD","total_amount":750.0,"confidence":0.92,"po_number":"PO-5099","line_items":[{"description":"Corrugated boxes","quantity":500,"unit_price":1.5,"amount":750.0}]}',
    # inv_007 - a real LLM often wraps JSON in a markdown code fence. Handle it.
    "inv_007": '```json\n{"invoice_number":"SF-2024-0090","vendor_name":"Summit Facilities Mgmt","invoice_date":"2024-03-11","currency":"USD","total_amount":4950.0,"confidence":0.91,"po_number":"PO-5004","line_items":[{"description":"Monthly facilities service","quantity":1,"unit_price":4950.0,"amount":4950.0}]}\n```',
    "inv_008": '{"invoice_number":"AC-2024-3391","vendor_name":"Acme Industrial Supply","invoice_date":"2024-03-20","currency":"USD","total_amount":4800.0,"confidence":0.96,"po_number":"PO-5001","line_items":[{"description":"Steel brackets","quantity":200,"unit_price":24.0,"amount":4800.0}]}',
    # inv_009 - the model returned BROKEN json (truncated). Your code must not crash.
    "inv_009": '{"invoice_number":"BR-2024-1205","vendor_name":"Brightline Office Co","invoice_date":"2024-03-19","currency":"USD","total_amount":540.0,"confidence":0.9,"po_number":"PO-5006","line_items":[{"description":"Desk organizers","quantity":60,"unit_price":9.0,',
    "inv_010": '{"invoice_number":"AC-2024-3450","vendor_name":"Acme Industrial Supply","invoice_date":"2024-03-21","currency":"USD","total_amount":5200.0,"confidence":0.95,"po_number":"PO-5007","line_items":[{"description":"Pallet racking unit","quantity":1,"unit_price":5200.0,"amount":5200.0}]}',
    "inv_011": '{"invoice_number":"BR-2024-1212","vendor_name":"Brightline Office Co","invoice_date":"2024-03-22","currency":"USD","total_amount":1450.0,"confidence":0.93,"po_number":"PO-5006","line_items":[{"description":"Toner cartridges","quantity":50,"unit_price":29.0,"amount":1450.0}]}',
    "inv_012": '{"invoice_number":"AC-2024-3460","vendor_name":"Acme Industrial Supply","invoice_date":"2024-03-23","currency":"USD","total_amount":300.0,"confidence":0.96,"po_number":null,"line_items":[{"description":"Shipping labels","quantity":10,"unit_price":30.0,"amount":300.0}]}',
}

_MOCK_FALLBACK = '{"invoice_number":"UNKNOWN","vendor_name":"UNKNOWN","invoice_date":"","currency":"USD","total_amount":0.0,"confidence":0.0,"po_number":null,"line_items":[]}'


class MockProvider:
    """Deterministic, offline LLM stand-in. Returns a canned response based on
    the invoice id present in the prompt."""

    def complete(self, prompt: str) -> str:
        for invoice_id, response in _MOCK_RESPONSES.items():
            if invoice_id in prompt:
                return response
        return _MOCK_FALLBACK


class RealProvider:
    """OPTIONAL BONUS. Wire a real LLM here using your own API key.

    Read the key/model/endpoint from environment variables (see `.env.example`)
    and POST to the provider with stdlib `urllib` - no vendor SDK is needed.
    The mock is the graded path; this exists if you want to demo a live model.
    """

    def __init__(self) -> None:
        # e.g. read os.environ["LLM_API_KEY"], model, base url here.
        pass

    def complete(self, prompt: str) -> str:
        raise NotImplementedError(
            "BONUS: implement a real provider with urllib (see .env.example)."
        )
