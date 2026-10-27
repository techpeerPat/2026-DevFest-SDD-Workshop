# Spec-Driven Multi-Agent Workshop: Run of Show and Lab Guide

## Workshop at a glance

In 90 minutes, each participant takes a support-triage multi-agent system from a blank folder to a running Google ADK app on their own laptop, using the Elephant and Goldfish skills to write and gate a spec before any code exists.

**Audience:** developers with some AI coding-agent experience, new to ADK. **Format:** hands-on, one laptop per person, facilitator-led with timed labs.

**What "local" means here.** The agents, tools, data and the ADK web UI all run on the participant's machine (localhost). Nothing is deployed to any cloud. The model calls still go over the internet to the free Gemini API, and the coding agent (Antigravity CLI) also needs internet. If you need a fully offline room, see the Ollama note in Troubleshooting.

**What they build.** A coordinator agent (`triage_router`) that reads a customer message and hands it to one of three specialists: `billing_agent`, `technical_agent` or `escalation_agent`. The tools read local JSON files and write tickets to a local file.

| Clock | Min | Segment | Skill or tool |
| --- | --- | --- | --- |
| 0:00 | 8 | Welcome, why spec-first, preflight check | none |
| 0:08 | 10 | ADK in 10 minutes (facilitator demo) | `adk web` |
| 0:18 | 15 | Lab 1: design with no code | `/elephant-grow` |
| 0:33 | 10 | Lab 2: write the design doc | `/elephant-teach` |
| 0:43 | 10 | Lab 3: fresh-session readiness gate (facilitator demos the cold read and the critic) | `/goldfish-ready` |
| 0:53 | 25 | Lab 4: build it and run it | `/implement-design` |
| 1:18 | 10 | Lab 5: hostile code review and fix | `/adversary-review` |
| 1:28 | 2 | Wrap and next steps | none |

**Skill coverage.** Participants run five of the seven skills. `/goldfish-understand` and `/goldfish-critic` are demonstrated live in Lab 3 on one volunteer's document, then left as homework. That is the trade-off for fitting 90 minutes.

## Facilitator notes

The biggest risk is free-tier quota, not content. Run the whole workshop yourself on a fresh Google account the week before and count how many agent requests each lab uses.

**Quota facts to plan around (verify the week of the event).**

- Antigravity CLI is included on the free Individual tier. Published numbers conflict: one guide says about 20 agent requests per day refreshing every five hours, another says a weekly agent quota. Treat the free tier as a thin allowance and measure it.
- The Gemini API free tier is limited per project, not per key, and Google no longer publishes a central table; the live numbers are at aistudio.google.com/rate-limit. Recent third-party tracking shows Gemini 3.8 Flash at about 5 requests per minute and 20 per day, and Gemini 3.5 Flash-Lite at about 10 per minute and 500 per day. The runtime model in this kit defaults to Flash-Lite for that reason.
- One user message to the multi-agent app costs about 2 to 4 model calls (router, specialist, tool follow-up). Ask people to space messages out by a few seconds to stay under the per-minute cap.

**Keep the coding agent frugal.** Every lab prompt below caps the number of questions and files so one lab uses few requests. Do not let participants re-run a skill "just to see".

**Checkpoint rule.** Each lab has a hard stop. At the stop, anyone who is not finished copies the checkpoint file and moves on. Nobody waits for stragglers.

| If at this time | and a participant has not | They do this |
| --- | --- | --- |
| 0:33 | finished the design discussion | Skip to Lab 2 and give `/elephant-teach` the one-line brief in the lab |
| 0:43 | produced `docs/DESIGN.md` | Copy `checkpoints/DESIGN.md` to `docs/DESIGN.md` |
| 0:53 | seen "Ready" from `/goldfish-ready` | Proceed anyway; the facilitator explains the gate on screen |
| 1:18 | a running app | Pair with a neighbour whose app runs, or use the reference solution |

**Fresh context is the whole point of Lab 3.** The Goldfish skills only mean something if the reader has not seen the conversation. Have participants open a second terminal tab and start a new `agy` session. Do not use `/clear` in the old session.

**Lab 3 demo script (5 minutes).** Pick a volunteer with a short design doc. On the projector, run `/goldfish-understand docs/DESIGN.md` in a fresh session and read out what it says it understands and what it flags as missing. Then run `/goldfish-critic docs/DESIGN.md` and show how findings are grouped by severity. Ask the room which finding they would fix first. Participants then run only `/goldfish-ready`.

**Staffing.** One helper per 12 participants. The helper's job is quota and install problems, so the facilitator keeps teaching.

**Honest framing for the room.** The skills are a discipline, not magic. Show one place where the gate caught something and one where it was overkill.

## Participant setup and Lab 0 preflight

Participants finish setup before the day, in about 10 minutes, from two public GitHub repos: the workshop kit (https://github.com/techpeerPat/2026-DevFest-SDD-Workshop) and the skills (https://github.com/techpeerPat/elephant-goldfish-skills). The kit's installer downloads the skills for them. Run a 15-minute "tech desk" before the start time for anyone whose preflight fails.

1. Install the prerequisites: Python 3.10+ and git.
2. Clone the kit into a folder named `triage-workshop` (it has no answer key; that lives on a separate branch).
3. Create and activate a virtual environment, then `pip install -r requirements.txt`.
4. Create a free Gemini API key at aistudio.google.com and paste it into `.env` (copied from `.env.example`).
5. Install the Antigravity CLI, then run `agy` once and finish the browser sign-in.
6. Download and install the skills with `python install_skills.py`. It clones the skills repo and copies the seven skills into `.agents/skills/`, on macOS, Linux and Windows.
7. Run `python check_setup.py`. Every line must say `[ ok ]`, including the line that confirms seven skills are installed.

**Pass condition for Lab 0:** `check_setup.py` prints "All set." and `agy` starts in the project folder and lists `/elephant-grow` when the person types `/ele`.

**Get a free Gemini API key (2 minutes, no credit card)**

1. Go to https://aistudio.google.com and sign in with a personal Google account. On the first visit, accept the terms and confirm your region. Work or school accounts may be restricted, so use a personal one if you can.
2. Click **Get API key** in the left sidebar (or open https://aistudio.google.com/app/apikey).
3. Click **Create API key**, then choose **Create key in new project**.
4. Copy the key. It starts with `AIza`.
5. Open `.env` in your project folder and paste it after `GOOGLE_API_KEY=`. Save the file.
6. Never commit or share the key. `.env` is already in `.gitignore`.

The free tier has per-minute and per-day limits that apply to the Google project, not the key. See your live limits at https://aistudio.google.com/rate-limit. Screens change, so if a button is named differently, look for "API keys".

**Which coding agent: `agy` or Gemini CLI?**

Use the Antigravity CLI (`agy`). Google retired Gemini CLI for free and personal accounts on 18 June 2026 and replaced it with `agy`. Gemini CLI is reported to still work only with paid API keys and with Gemini Code Assist Standard or Enterprise licences, which is not the free setup this workshop uses. The skills are installed into `.agents/skills/`, which is where `agy` looks. Prefer Claude Code? Use `python install_skills.py --agent claude`.

Using Claude Code instead of Antigravity? Run `python install_skills.py --agent claude` in step 6. The skills then install into `.claude/skills/` instead of `.agents/skills/`, and `check_setup.py` accepts either. Both install into the project folder only, never globally. Each participant should pick one agent and stay on it.

Commands (macOS or Linux; Windows variants are in the note below the folder listing):

```
git clone https://github.com/techpeerPat/2026-DevFest-SDD-Workshop.git triage-workshop
cd triage-workshop
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # paste your key into .env
curl -fsSL https://antigravity.google/cli/install.sh | bash
# open a NEW terminal, activate the venv again, then:
python install_skills.py    # downloads elephant-goldfish-skills
python check_setup.py
```

**Project folder at the start of the workshop:**

```
triage-workshop/
  .agents/skills/        (seven skills)
  .env                   (your key, never commit)
  data/                  (customers.json, kb.json)
  tickets/
  checkpoints/DESIGN.md
  check_setup.py
  requirements.txt
```

On Windows, use PowerShell, activate with `.venv\Scripts\Activate.ps1`, and install the CLI with `irm https://antigravity.google/cli/install.ps1 | iex`. Git must be installed for the skill clone step.

## ADK in 10 minutes (facilitator demo, 0:08)

The goal is that nobody is surprised by the code the coding agent writes in Lab 4. Live-code or screen-share a tiny two-agent example from the reference solution while you cover five ideas.

1. **An agent is a name, a model, an instruction and optional tools.** `from google.adk.agents import Agent`.
2. **A tool is a plain Python function.** ADK reads its name, type hints and docstring to tell the model how to call it. A vague docstring means a badly used tool.
3. **`sub_agents=[...]` makes a team.** The parent can transfer the conversation to a child. The model decides who, using each child's `description`, so descriptions are routing rules.
4. **A package is a folder with `__init__.py` and `agent.py`.** `agent.py` must expose a variable named `root_agent`. `__init__.py` does `from . import agent`.
5. **`adk web` runs from the parent folder** of the agent package, serves a chat UI on http://localhost:8000, and shows a trace of every transfer and tool call. `adk run support_triage` is the terminal version. ADK Web is for development, not production.

Show the trace view. It is the proof, in Lab 4, that the router really handed off to a specialist.

```
from google.adk.agents import Agent

def check_invoice(customer_id: str) -> dict:
    """Compare a customer's last invoice with their plan price."""
    ...

billing_agent = Agent(
    name="billing_agent",
    model="gemini-3.5-flash-lite",
    description="Handles invoice and charge questions.",
    instruction="Look the customer up, then call check_invoice.",
    tools=[check_invoice],
)

root_agent = Agent(
    name="triage_router",
    model="gemini-3.5-flash-lite",
    description="Routes support messages.",
    instruction="Do not answer yourself. Transfer to the right specialist.",
    sub_agents=[billing_agent],
)
```

This is the shape of the reference solution. It loads and is discovered by `adk web` on google-adk 2.13.0 (Python 3.13); live model calls were not tested.

## Labs 1 to 5

The rule for the whole session: no code until the design passes the gate. Every lab starts in the `triage-workshop` folder. Type each prompt into `agy` (or Claude Code). Before Lab 1, run `/model` once in `agy`, pick a model, and use that same one for all five labs so results are comparable across the room. Which models appear, and the free quota for each, depends on the account: check before the day. Prompts are written to cap questions and files, which keeps free-tier request use low.

### Lab 1: Design with no code (0:18, 15 min, `/elephant-grow`)

Goal: leave with decisions, not code. The skill refuses to write code and challenges your assumptions.

Prompt:

```
/elephant-grow I want a local-only customer support triage system built with Google ADK in Python. A coordinator agent routes each message to a billing, technical or escalation specialist. Data is in data/customers.json and data/kb.json, tickets go to a local file, and nothing is deployed. Ask at most 5 questions at a time. Challenge my routing rules, my tool inputs and outputs, and how we will know it works.
```

Settle these five things before you stop. If the agent has not raised one, raise it yourself.

- **Routing:** which messages go to which specialist, and what happens when a message fits two.
- **Tool contracts:** inputs, outputs and the error case for each of the four tools.
- **Severity rules** for tickets.
- **Out of scope:** at least two things you are choosing not to build (refunds and customer verification are good candidates).
- **Success checks:** three messages and the exact routing you expect.

Hard stop at 0:33. Not finished? Go to Lab 2 with the five bullets you have.

### Lab 2: Write the design doc (0:33, 10 min, `/elephant-teach`)

Goal: turn the conversation into `docs/DESIGN.md`. Stay in the same session so the skill has the discussion to draw from.

Prompt:

```
/elephant-teach Write the design document to docs/DESIGN.md from our discussion.
```

Check the file has the five required sections: Problem, Technical Plan, Alternatives, Detailed Implementation, Evaluation Criteria. Open Questions is optional. Then check two things yourself:

- Detailed Implementation lists every file to create, including `support_triage/__init__.py` and `support_triage/agent.py`.
- Each Evaluation Criterion is something a person or a test can check, not an adjective.

Commit it: `git add -A && git commit -m "design doc"`. Hard stop at 0:43. No file? Copy `checkpoints/DESIGN.md` to `docs/DESIGN.md`.

### Lab 3: The readiness gate (0:43, 10 min, `/goldfish-ready`)

Goal: find out whether a reader with no memory of your conversation could build this correctly. The facilitator first demonstrates `/goldfish-understand` and `/goldfish-critic` on a volunteer's document.

1. Open a **new terminal tab**, activate the venv, `cd` into the project and start a fresh `agy`. Do not reuse the Lab 1 and 2 session.
2. Run:

```
/goldfish-ready docs/DESIGN.md
```

3. The verdict is "Ready" or "Not ready". If "Not ready", read the reasons, go back to your original session, fix the document (ask `/elephant-teach` to update the specific sections), and run the gate once more. One loop only.

What to notice: every gap it lists is a bug you would have found an hour into coding.

### Lab 4: Build it and run it (0:53, 25 min, `/implement-design`)

Goal: a running multi-agent app that matches the document and nothing else.

1. In the original session or a new one, run:

```
/implement-design docs/DESIGN.md
```

2. Run the offline tests the agent wrote (no API key needed): `python tests/test_tools.py` or `python -m pytest tests -q`.
3. From the **project root** (the folder that contains `support_triage/`), start the UI: `adk web`. Open http://localhost:8000 and pick `support_triage` at the top left.
4. Send these three messages, a few seconds apart, and open the trace for each:

| Message | Expected route | Expected result |
| --- | --- | --- |
| I was charged twice, my email is maya@example.com | `billing_agent` | States an overcharge of 29 |
| My app crashes when I launch it | `technical_agent` | Quotes the crash article |
| Your whole service is down and we lost data | `escalation_agent` | Returns a ticket id; a line appears in `tickets/tickets.jsonl` |

5. Commit: `git add -A && git commit -m "implementation"`.

**The spec-driven rule.** If something is wrong, do not ask the agent to "just fix it" in chat. Decide whether the document was wrong or the code was wrong. If the document was wrong, edit the document, then re-run `/implement-design`. If the code ignored the document, say so and have it conform. That habit is the point of the day.

Common snags: running `adk web` from inside `support_triage/` (nothing is listed), a missing `root_agent` variable, a 429 from sending messages too fast, and a model name that does not exist for the key (404). All are covered in Troubleshooting.

Hard stop at 1:18. Not running? Pair with a neighbour whose app runs and send their messages together.

### Lab 5: Hostile review and wrap (1:18, 10 min, `/adversary-review`)

Goal: see what a hostile reviewer finds in code that already "works".

1. Run, in a fresh session:

```
/adversary-review support_triage/ tests/
```

2. The review returns numbered findings and ends with a verdict, either "APPROVED" or blocked. You will not reach "APPROVED" in ten minutes, and that is fine. Pick the **two** findings you consider most serious and fix them, either by hand or by naming them to the agent.
3. Write one sentence in `docs/DESIGN.md` under Open Questions for any finding you chose not to fix.

**Wrap (1:28, 2 min).** Ask the room: what did the document catch that the code never would have? Then assign homework.

- Run `/goldfish-understand` and `/goldfish-critic` on your own `docs/DESIGN.md`.
- Add a fourth specialist, for example `account_agent`, using the full loop: grow, teach, understand, critic, ready, implement, adversary-review.
- Compare your `support_triage/` with the answer key in `reference/`.

## Troubleshooting and fallbacks

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `agy: command not found` | Installer put the binary in `~/.local/bin` (macOS, Linux) or `%LOCALAPPDATA%\Antigravity` (Windows) and the shell has not picked it up | Open a new terminal. If still missing, add that folder to PATH. |
| Typing `/elephant-grow` does nothing | Skills not in `.agents/skills/` of the folder `agy` was started from | Run `ls .agents/skills`, expect seven folders, then restart `agy` from the project root. |
| Coding agent stalls, queues, or says quota used | Free-tier Antigravity allowance spent | Switch to the checkpoint for that lab (see Facilitator notes). Pair with a neighbour. Do not retry in a loop. |
| `adk web` lists no agents | Started from inside `support_triage/` | `cd ..` to the project root and run it again. |
| `ModuleNotFoundError: google.adk` | Virtual environment not active | `source .venv/bin/activate`. |
| 429 RESOURCE_EXHAUSTED from Gemini | Per-minute or per-day free quota | Wait a minute and send fewer messages. If it says daily, change `WORKSHOP_MODEL` to another model that AI Studio shows with quota. |
| 429 with "limit: 0" | That model has no free quota for this key | Use `gemini-3.5-flash-lite` or a model your AI Studio rate-limit page shows as available. |
| 404 model not found | Typo or retired model name in `.env` | Check the model list in AI Studio and fix `WORKSHOP_MODEL`. |
| 403 PERMISSION_DENIED, "project denied access" | Google flagged or restricted the project, sometimes pending age verification | Create a key in a different project or account. Keep 2 spare keys at the tech desk. |
| 400 FAILED_PRECONDITION on a free project | Reported by other users on Google's developer forum in October 2026; cause unconfirmed | Try the key in the AI Studio playground, then a new key in a new project. |
| Corporate laptop blocks the install script or Google sign-in | Security policy | Ask the attendee to pair, or ask their IT team ahead of time. |

**Fallback coding agents.** Claude Code is supported: `python install_skills.py --agent claude` installs the skills into `.claude/skills/` in the project (file placement tested; a live Claude Code run is not yet). Other agents that read `.agents/skills/` also work. A participant who already has a paid agent can use it for Labs 1 to 5. The README in the skills repo has the commands.

**Offline rooms.** This design cannot run in a room with no internet, because `agy` and the Gemini API both need it. Swapping the runtime model for a local Ollama model is possible in ADK, but it is untested here, needs a large download and a laptop with 16GB or more RAM, and tool calling is weaker on small models. Treat it as a separate workshop.

## Appendix: starter kit, verification status, sources

**Starter kit (public repo: github.com/techpeerPat/2026-DevFest-SDD-Workshop).** `data/customers.json` (six customers; C-1001 and C-1005 are overcharged), `data/kb.json` (four articles), `check_setup.py`, `install_skills.py`, `.env.example`, `requirements.txt`, `README.md`, `LICENSE`, `checkpoints/DESIGN.md` (fallback design doc). The working answer key is on the `answer-key` branch.

**Design doc format** produced by `/elephant-teach`: Problem, Technical Plan, Alternatives, Detailed Implementation, Evaluation Criteria, and optional Open Questions.

**What was verified and what was not.**

| Item | Status |
| --- | --- |
| Reference agents load, `adk web` discovers `support_triage` | Verified on google-adk 2.13.0, Python 3.13 |
| Four tools pass the offline tests | Verified |
| `check_setup.py` logic | Verified up to the Gemini call; the model call itself is not exercised |
| A live Gemini call, routing quality and transfers in the trace | Not tested (no API key available when this was built). Pilot it. |
| `agy` install, sign-in, slash-command discovery, skill behaviour and request use | Not tested. Pilot it. |
| Free-tier numbers | Taken from third-party pages dated October 2026 that disagree in places. Re-check the week of the event. |

**Sources** (read as search excerpts, not opened in full):

- [Elephant and Goldfish skills repo](https://github.com/techpeerPat/elephant-goldfish-skills)
- [ADK Python quickstart](https://adk.dev/get-started/python/index.md)
- [Antigravity CLI install guide](https://www.layer3labs.io/guides/google-antigravity-cli)
- [Antigravity pricing and free tier](https://www.cloudzero.com/blog/google-antigravity-pricing/)
- [Antigravity CLI commands and free-tier request limits](https://www.gradually.ai/en/antigravity-cli-commands/)
- [Gemini API free-tier limits](https://www.scriptbyai.com/gemini-api-free-tier-limits/)
- [Gemini API rate limits by tier](https://www.developersdigest.tech/rate-limits/google)
- [Gemini 429 "limit: 0" write-up](https://dev.to/nils44344/gemini-api-429-resourceexhausted-why-your-limit-is-0-68o)
