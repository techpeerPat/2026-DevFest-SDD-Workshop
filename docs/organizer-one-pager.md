# Organizer One-Pager: Spec-Driven Multi-Agent Workshop

## Event snapshot

A 90-minute, hands-on workshop where each participant builds a three-specialist support-triage system with Google ADK on their own laptop, driven by a written spec and gated by the Elephant and Goldfish skills. Nothing is deployed to any cloud.

| | |
| --- | --- |
| Audience | Developers with some AI coding-agent experience, new to ADK |
| Length | 90 minutes, plus a 15-minute tech desk before start |
| Group size | Suggested cap of 24 with 2 helpers (1 helper per 12 people); adjust to your room |
| Format | One laptop per person, facilitator-led timed labs |
| Participant cost | $0 (free tiers only, no credit card) |
| Materials | Slide deck, run-of-show and lab guide, public starter-kit repo (github.com/techpeerPat/2026-DevFest-SDD-Workshop) |

## What each participant needs

| Need | Requirement | Cost |
| --- | --- | --- |
| Laptop | macOS, Windows 10+ with PowerShell, or 64-bit Linux (glibc 2.28+). No GPU. Admin rights help but the CLI installs per-user. | Own device |
| Python | 3.10 or newer, with `venv` | Free |
| Git and a terminal | Git must be installed (the skills are cloned from GitHub) | Free |
| Browser | Any, for the one-time Google sign-in and the ADK web UI on localhost | Free |
| Google account | A personal Google account for Antigravity sign-in. Work or school accounts may be restricted: check with a test account first. | Free |
| Antigravity CLI (`agy`) | Installed from Google's one-line script; free Individual tier. Participants pick one model with `/model` and use it for all labs. Claude Code is a supported alternative (file placement tested, live run not yet). | Free, limited quota |
| Gemini API key | Created at aistudio.google.com, no billing needed | Free, limited quota |
| Python packages | `google-adk`, `pytest`, installed with pip | Free |
| Elephant and Goldfish skills | Downloaded from github.com/techpeerPat/elephant-goldfish-skills by `python install_skills.py`, into the project folder only: `.agents/skills/` (agy) or `.claude/skills/` (Claude Code, with `--agent claude`). Never global. | Free |
| Network | Outbound HTTPS to Google (sign-in, Antigravity, Gemini API), GitHub and PyPI | Venue Wi-Fi |

## Free-tier limits: the main risk

The workshop runs on two free quotas, and both have been cut before. Pilot the full run on a fresh account the week of the event and re-check the numbers below.

| Quota | What sources report (October 2026) | Why it matters |
| --- | --- | --- |
| Antigravity CLI, free Individual tier | About 20 agent requests per day, refreshing every five hours, per one guide; a "weekly agent quota" per another. Sources disagree. | The coding agent runs in Labs 1 to 5. A participant can run out mid-session. |
| Gemini API, Flash-Lite models | About 10 requests per minute and 500 per day | The kit's default runtime model. A 3-message test uses roughly 6 to 12 calls. |
| Gemini API, 3.8 and 3.6 Flash | About 5 requests per minute and 20 per day | Too small for this workshop. Do not use as the runtime model. |
| Gemini API limits scope | Per Google project, not per key. Live values are at aistudio.google.com/rate-limit | Extra keys in the same project add nothing. |

**Mitigations built in:** lab prompts cap questions and files; every lab has a checkpoint file; the reference solution works as an answer key; any agent that reads `.agents/skills/` can replace `agy`. **Data note:** free-tier Gemini API usage is handled differently from paid usage, so tell participants not to put real customer data in the exercise.

## Checklists

**Organizer, before the event**

- [ ] One week out: run the full workshop yourself on a fresh Google account and note requests used per lab.
- [ ] One week out: confirm current Antigravity and Gemini free-tier limits; adjust the model name in `.env.example` if needed.
- [ ] Five days out: email participants the repo link and the 10-minute setup steps; ask them to run `python check_setup.py` and reply with a screenshot.
- [ ] Two days out: chase anyone whose check failed; offer the tech desk.
- [ ] Create 2 spare Gemini API keys in separate projects and 2 spare Google accounts for the tech desk.
- [ ] Confirm venue Wi-Fi allows Google, GitHub and PyPI, and can carry the whole room installing at once.

**Day-of room needs**

- [ ] Projector or screen with HDMI and USB-C adapters, plus a second screen for the facilitator's terminal.
- [ ] Power strip at every table. Agents and a local web server drain laptops.
- [ ] A zip of the cloned repo on a USB stick as a Wi-Fi-failure backup, with `.agents/skills/` already installed (the skills installer needs the network) and the `checkpoints/DESIGN.md` file.
- [ ] Printed one-page lab timeline, or the deck's agenda slide on screen throughout.
- [ ] A visible countdown timer for the hard stops.
- [ ] Tech desk opens 15 minutes before start.
