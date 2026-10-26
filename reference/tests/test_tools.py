"""Offline tests: no API key, no model calls. Run: python reference/tests/test_tools.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from support_triage import tools  # noqa: E402


def test_overcharge_detected():
    r = tools.check_invoice("C-1001")
    assert r["discrepancy"] and r["overcharge_amount"] == 29


def test_clean_invoice():
    assert tools.check_invoice("C-1002")["discrepancy"] is False


def test_lookup_by_email_and_missing():
    assert tools.lookup_customer("LENA@example.com")["status"] == "found"
    assert tools.lookup_customer("nobody@example.com")["status"] == "not_found"


def test_kb_search():
    assert tools.search_kb("my app crashes on launch")["matches"][0]["id"] == "KB-03"
    assert tools.search_kb("zzzz qqqq")["matches"] == []


def test_ticket_validation_and_write(tmp_path, monkeypatch=None):
    tools.TICKETS_FILE = tmp_path / "t.jsonl"
    assert tools.create_ticket("C-1", "x", "urgent")["status"] == "error"
    ok = tools.create_ticket("C-1", "outage", "HIGH")
    assert ok["status"] == "created"
    assert json.loads(tools.TICKETS_FILE.read_text().splitlines()[0])["severity"] == "high"


if __name__ == "__main__":
    import tempfile
    test_overcharge_detected(); test_clean_invoice(); test_lookup_by_email_and_missing(); test_kb_search()
    test_ticket_validation_and_write(Path(tempfile.mkdtemp()))
    print("all tool tests passed")
