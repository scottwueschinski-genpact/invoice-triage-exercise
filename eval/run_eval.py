"""Evaluation harness: run the agent over the invoice batch and score it against
the visible gold labels. Pass bar is >= 0.80 accuracy on the labelled invoices.

Run with:  make eval   (or:  PYTHONPATH=src python eval/run_eval.py)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent.agent import triage_batch          # noqa: E402
from agent.provider import MockProvider        # noqa: E402
from agent.audit import format_audit_record    # noqa: E402

PASS_BAR = 0.80


def _load(path: Path):
    with open(path) as fh:
        return json.load(fh)


def main() -> int:
    invoices = _load(ROOT / "data" / "invoices.json")
    vendor_master = _load(ROOT / "data" / "reference" / "vendor_master.json")
    purchase_orders = _load(ROOT / "data" / "reference" / "purchase_orders.json")
    gold = {k: v for k, v in _load(ROOT / "data" / "gold" / "labels.json").items()
            if not k.startswith("_")}

    records = triage_batch(invoices, MockProvider(), vendor_master, purchase_orders)

    print("\nDECISIONS")
    print("-" * 92)
    for record in records:
        print(format_audit_record(record))

    print("\nSCORING (vs visible gold labels)")
    print("-" * 92)
    correct = 0
    scored = 0
    by_id = {r.invoice_id: r for r in records}
    for invoice_id, expected in sorted(gold.items()):
        record = by_id.get(invoice_id)
        got = record.decision.action if record else "(missing)"
        ok = got == expected["action"]
        scored += 1
        correct += 1 if ok else 0
        mark = "PASS" if ok else "FAIL"
        note = "" if ok else f"   expected={expected['action']}"
        print(f"  [{mark}] {invoice_id:<8} got={got:<13}{note}")

    accuracy = correct / scored if scored else 0.0
    print("-" * 92)
    print(f"Accuracy: {correct}/{scored} = {accuracy:.0%}   (pass bar: {PASS_BAR:.0%})")
    passed = accuracy >= PASS_BAR
    print("RESULT:", "PASS ✓" if passed else "FAIL ✗")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
