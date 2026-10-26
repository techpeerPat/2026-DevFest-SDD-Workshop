"""Preflight check for the spec-driven multi-agent workshop. Run: python check_setup.py

Checks Python, ADK, the agy CLI, git, and (optionally) makes ONE tiny Gemini call.
The Gemini call uses 1 request of your free daily quota. Skip it with --no-model.
"""
import os
import shutil
import sys

OK, BAD = "[ ok ]", "[FAIL]"
failures = 0


def report(passed: bool, label: str, hint: str = "") -> None:
    global failures
    print(f"{OK if passed else BAD} {label}" + ("" if passed else f"\n       -> {hint}"))
    failures += 0 if passed else 1


def load_dotenv_if_present() -> None:
    path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


load_dotenv_if_present()
report(sys.version_info >= (3, 10), f"Python {sys.version.split()[0]} (need 3.10+)", "Install Python 3.10 or newer.")

try:
    import google.adk  # noqa: F401
    report(True, f"google-adk {google.adk.__version__}")
except Exception:
    report(False, "google-adk importable", "Activate your venv, then: pip install google-adk")

report(shutil.which("adk") is not None, "adk command on PATH", "Activate your venv; the adk command comes with google-adk.")
report(shutil.which("agy") is not None, "agy (Antigravity CLI) on PATH", "Install from Google's Antigravity CLI page, open a NEW terminal, then run: agy --version")
report(shutil.which("git") is not None, "git installed", "Install git.")
report(bool(os.environ.get("GOOGLE_API_KEY")), "GOOGLE_API_KEY is set", "Copy .env.example to .env and paste your AI Studio key.")

if "--no-model" not in sys.argv and os.environ.get("GOOGLE_API_KEY"):
    try:
        from google import genai
        model = os.environ.get("WORKSHOP_MODEL", "gemini-3.5-flash-lite")
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        reply = client.models.generate_content(model=model, contents="Reply with the single word: ready")
        report("ready" in (reply.text or "").lower(), f"Gemini call to {model} works")
    except Exception as exc:  # noqa: BLE001
        report(False, "Gemini call works", f"{type(exc).__name__}: {str(exc)[:160]} (429 = quota, 403 = project blocked, 404 = model name)")

print("\nAll set." if failures == 0 else f"\n{failures} check(s) failed. Fix them before the workshop.")
sys.exit(1 if failures else 0)
