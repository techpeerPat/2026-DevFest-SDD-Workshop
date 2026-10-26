"""Local-only tools for the support triage system. No network calls."""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
TICKETS_FILE = Path(__file__).resolve().parent.parent.parent / "tickets" / "tickets.jsonl"
VALID_SEVERITIES = {"low", "medium", "high"}


def _load(name: str) -> list:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def lookup_customer(identifier: str) -> dict:
    """Find a customer by id (for example C-1001) or by email address.

    Args:
        identifier: A customer id or an email address.

    Returns:
        A dict with status 'found' and the customer record, or status 'not_found'.
    """
    needle = identifier.strip().lower()
    for customer in _load("customers.json"):
        if needle in (customer["id"].lower(), customer["email"].lower()):
            return {"status": "found", "customer": customer}
    return {"status": "not_found", "identifier": identifier}


def check_invoice(customer_id: str) -> dict:
    """Compare a customer's last invoice with their plan price.

    Args:
        customer_id: A customer id such as C-1001.

    Returns:
        A dict with the plan price, last invoice and whether they differ.
    """
    result = lookup_customer(customer_id)
    if result["status"] != "found":
        return result
    c = result["customer"]
    diff = c["last_invoice_amount"] - c["monthly_price"]
    return {
        "status": "ok",
        "customer_id": c["id"],
        "plan": c["plan"],
        "monthly_price": c["monthly_price"],
        "last_invoice_amount": c["last_invoice_amount"],
        "discrepancy": diff != 0,
        "overcharge_amount": diff if diff > 0 else 0,
    }


def search_kb(query: str) -> dict:
    """Search the local knowledge base by keyword.

    Args:
        query: Words describing the customer's technical problem.

    Returns:
        Up to 3 matching articles, best match first.
    """
    words = {w for w in query.lower().split() if len(w) > 2}
    scored = []
    for article in _load("kb.json"):
        hits = sum(1 for k in article["keywords"] if any(w in k or k in w for w in words))
        if hits:
            scored.append((hits, article))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return {"status": "ok", "matches": [a for _, a in scored[:3]]}


def create_ticket(customer_id: str, summary: str, severity: str) -> dict:
    """Create an escalation ticket in the local tickets file.

    Args:
        customer_id: A customer id such as C-1001, or 'unknown'.
        summary: One or two sentences describing the problem.
        severity: One of 'low', 'medium' or 'high'.

    Returns:
        A dict with the new ticket id, or an error if severity is invalid.
    """
    severity = severity.strip().lower()
    if severity not in VALID_SEVERITIES:
        return {"status": "error", "message": f"severity must be one of {sorted(VALID_SEVERITIES)}"}
    ticket = {
        "ticket_id": f"T-{uuid.uuid4().hex[:6].upper()}",
        "customer_id": customer_id,
        "summary": summary,
        "severity": severity,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    TICKETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TICKETS_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(ticket) + "\n")
    return {"status": "created", "ticket_id": ticket["ticket_id"]}
