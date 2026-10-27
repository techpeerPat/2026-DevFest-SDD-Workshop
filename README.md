# 2026 DevFest: Spec-Driven Development Workshop

Build a multi-agent support-triage system with Google ADK in 90 minutes, entirely on your laptop. A written spec comes first; the Elephant and Goldfish skills gate it before any code exists.

Agents, tools, data and the ADK web UI run locally. Model calls go to the free Gemini API, and the coding agent (Antigravity CLI, `agy`) needs internet.

## What is in this repo

| Path | What it is |
| --- | --- |
| `data/` | Fake customers and knowledge-base articles. Do not edit. |
| `check_setup.py` | Preflight check. Run it before the workshop. |
| `.env.example` | Copy to `.env` and add your free Gemini API key. |
| `checkpoints/DESIGN.md` | Fallback design doc if a lab stalls. |
| `tickets/` | Where escalation tickets are written. |
| `docs/` | Workshop guide, organizer one-pager and slide outline. |

A working answer key lives on the `answer-key` branch. Please do not open it until after the workshop.

## Setup (10 minutes, before the workshop)

```bash
# 1. Get the kit
git clone https://github.com/techpeerPat/2026-DevFest-SDD-Workshop.git triage-workshop
cd triage-workshop

# 2. Python environment (3.10+)
python3 -m venv .venv
source .venv/bin/activate           # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Free Gemini API key: https://aistudio.google.com -> Get API key
cp .env.example .env                # then paste the key into .env

# 4. Antigravity CLI (macOS / Linux). Windows PowerShell: irm https://antigravity.google/cli/install.ps1 | iex
curl -fsSL https://antigravity.google/cli/install.sh | bash
# open a NEW terminal, re-activate the venv, then:
agy --version

# 5. The Elephant and Goldfish skills
#    Downloads https://github.com/techpeerPat/elephant-goldfish-skills and copies the
#    seven skills into .agents/skills/ (works on macOS, Linux and Windows; needs git)
python install_skills.py              # Antigravity (agy)
# Using Claude Code instead?  python install_skills.py --agent claude

# 6. Verify
python check_setup.py
```

Skills install into this project folder only (`.agents/skills/` for agy, `.claude/skills/` for Claude Code), never globally. Check they loaded: start your agent from this folder and type `/ele`. You should see `/elephant-grow` and `/elephant-teach`.

The first run of `agy` opens a browser to sign in with a Google account.

### Pick one model for the coding agent

`agy` can use more than one model. Run `/model` inside `agy`, choose one, and use that same model for all five labs, so results are comparable across the room. Which models appear, and how much free quota each has, depends on your account. Check before the day.

## During the workshop

Work only inside your clone. Put your design doc at `docs/DESIGN.md`. The agent package must be a folder named `support_triage/` in the project root so that `adk web`, run from the root, finds it. Keep your work local; there is nothing to push.

## Licence

MIT. See [LICENSE](LICENSE).
