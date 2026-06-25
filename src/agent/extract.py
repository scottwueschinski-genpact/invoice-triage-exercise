"""Structured extraction from a raw invoice. TODO 1 - see TASK.md."""
from typing import Optional
from .schema import InvoiceExtraction
from .provider import LLMProvider

# A prompt template is provided so you can focus on the engineering, not wording.
EXTRACTION_PROMPT = """You are an accounts-payable extraction assistant.
Extract the following fields from the invoice text and return ONLY a JSON object:
invoice_number, vendor_name, invoice_date (ISO), currency, total_amount (number),
confidence (0-1), po_number (or null), line_items (list of
{{description, quantity, unit_price, amount}}).

INVOICE:
{raw_text}
"""


def extract_invoice(raw_text: str, provider: LLMProvider) -> Optional[InvoiceExtraction]:
    """TODO 1 - turn raw invoice text into a validated InvoiceExtraction.

    Steps you need to implement:
      1. Build the prompt (use EXTRACTION_PROMPT) and call `provider.complete(prompt)`.
      2. Parse the model's response into JSON. NOTE: the model is not always clean -
         it may wrap the JSON in ```json ... ``` fences, and it may occasionally
         return broken/truncated JSON.
      3. Validate it: the required fields must be present and the right types.
      4. Return a populated InvoiceExtraction on success.
      5. If you CANNOT get valid structured data, return None - do not crash, and do
         not pass made-up data downstream. (A None here becomes an `escalate` later.)
    """
    raise NotImplementedError("TODO 1: implement extract_invoice (see TASK.md)")
