# Slide outline and speaker notes

Text of every slide in the DevFest deck, with speaker notes. The deck itself is built on the DevFest 2026 template.

## Slide 1

- Hands-on workshop
- Spec Driven Development with the Elephant - Goldfish Model
- Pat Bentley
- Google ADK · 90 minutes

**Speaker notes:** Welcome. Everyone should have run check_setup.py already. Say the promise of the day: nobody writes code until the design passes a gate. Tech desk is at the back for anyone whose preflight failed.

## Slide 2

- Before we start · about 10 min
- Setup 1 of 3: Get the kit
- Install Python 3.10+ and git
- Clone the workshop repo
- Create a virtual environment
- Add your free Gemini key to .env
- TERMINAL
- git clone https://github.com/techpeerPat/2026-DevFest-SDD-Workshop.git triage-workshop
- cd triage-workshop
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- cp .env.example .env
- Free Gemini key: aistudio.google.com. Windows: activate with .venv\Scripts\Activate.ps1

**Speaker notes:** Leave this slide up while people arrive. The repo is public and has no answer key; the answer key is on a separate branch. The Gemini key is free from aistudio.google.com: Get API key, paste it into .env. Windows users use PowerShell. Anyone without git or Python goes to the tech desk.

## Slide 3

- Before we start · about 10 min
- Setup 2 of 3: Agent and skills
- Install the Antigravity CLI (or use Claude Code)
- Run agy once and sign in with Google
- Download the skills with the kit's installer
- Start agy here and type /ele
- TERMINAL
- curl -fsSL https://antigravity.google/cli/install.sh | bash
- agy --version
- python install_skills.py
- # Claude Code instead of agy:
- python install_skills.py --agent claude
- Windows PowerShell
- irm https://antigravity.google/cli/install.ps1 | iex
- Skills repo: github.com/techpeerPat/elephant-goldfish-skills. Installs into this project only: .agents/skills/ (agy) or .claude/skills/ (Claude).

**Speaker notes:** Open a NEW terminal after installing agy so it is on the PATH. First run opens a browser for Google sign-in. install_skills.py downloads the elephant-goldfish-skills repo, copies the seven skill folders into .agents/skills/ inside the project, and works on macOS, Linux and Windows, and only touches the project folder, never global config. Participants using Claude Code add --agent claude, which installs into .claude/skills/ instead; pick one agent and stay on it. Success test: start agy from the project folder, type /ele and see /elephant-grow and /elephant-teach. If not, agy was started from the wrong folder.

## Slide 4

- Before we start · about 10 min
- Setup 3 of 3: Run the preflight
- Run python check_setup.py
- Every line must say [ ok ]
- Fix any [FAIL] with the hint shown
- Still red? Go to the tech desk
- EXPECTED (ABBREVIATED)
- [ ok ] Python 3.12
- [ ok ] google-adk
- [ ok ] agy on PATH
- [ ok ] 7 skills installed
- [ ok ] GOOGLE_API_KEY is set
- [ ok ] Gemini call works
- All set.
- The Gemini check uses one free request. Skip it with --no-model.

**Speaker notes:** Everyone should see All set. before the workshop starts. Common fails: venv not activated (google-adk or adk missing), agy installed but terminal not reopened, wrong or missing key, and a 429 from free-tier quota. The skills line failing means install_skills.py was not run from the project folder.

## Slide 5

- What you leave with
- 01
- A gated design doc
- A written spec that a stranger could build from, checked before any code exists.
- 02
- A running agent team
- A router and three specialists in Google ADK, served from localhost with a visible trace.
- 03
- A loop you can reuse
- Grow, teach, gate, implement, review. Seven skills, five of them hands-on today.
- Nothing is deployed. Everything runs on your machine.

**Speaker notes:** Set expectations: this is a discipline workshop that happens to produce an ADK app. Be clear that model calls still go to the free Gemini API over the internet; the agents, tools, data and UI are local.

## Slide 6

- Chatting your way to code fails quietly
- THE USUAL LOOP
- Describe the idea in chat
- Agent writes code
- Find a surprise
- Patch, patch, patch
- Decisions get made by accident, inside code nobody asked for.
- THE SPEC-FIRST LOOP
- Decide, with no code allowed
- Write the decisions down
- Gate them with a cold reader
- Build exactly that, then attack it
- Surprises show up in a document, where they cost one edit.

**Speaker notes:** Keep this to two minutes. The point: when the document is wrong you edit a paragraph; when code is wrong you edit a system. Ask who has been bitten by an agent that quietly widened scope.

## Slide 7

- Hands-on workshop
- Spec first. Then agents. No code until the design passes the gate.

**Speaker notes:** The rule for the whole session. If anyone starts writing code before the gate, point back to this slide.

## Slide 8

- 01
- The plan
- Seven skills, the agenda and the system we build

## Slide 9

- Seven skills, one loop
- | Step | Command | What it does | Today |
- | --- | --- | --- | --- |
- | 1 | /elephant-grow | No-code design discussion | Hands-on |
- | 2 | /elephant-teach | Writes the design document | Hands-on |
- | 3 | /goldfish-understand | Zero-context cold read | Demo |
- | 4 | /goldfish-critic | Hostile architecture review | Demo |
- | 5 | /goldfish-ready | Ready or not ready, before code | Hands-on |
- | 6 | /implement-design | Builds only what the doc says | Hands-on |
- | 7 | /adversary-review | Hostile code review | Hands-on |
- Steps 3 to 5 only work in a fresh session: the reader must not remember your conversation.

**Speaker notes:** Walk the table once. Emphasise the fresh-context rule: the goldfish skills are named for a reader with no memory. If a review in the same session passes, it proves nothing. Steps 3 and 4 are shown on the projector; participants run only step 5 in Lab 3 to protect their free-tier quota.

## Slide 10

- The next 90 minutes
- | Clock | Segment | Tool |
- | --- | --- | --- |
- | 0:00 | Welcome and why spec-first | none |
- | 0:08 | ADK in 10 minutes (demo) | adk web |
- | 0:18 | Lab 1: design, no code | /elephant-grow |
- | 0:33 | Lab 2: write the design doc | /elephant-teach |
- | 0:43 | Lab 3: readiness gate, fresh session | /goldfish-ready |
- | 0:53 | Lab 4: build it and run it | /implement-design |
- | 1:18 | Lab 5: hostile review | /adversary-review |
- | 1:28 | Wrap and homework | none |

**Speaker notes:** Point out that every lab has a hard stop and a checkpoint file. Put a visible countdown on a second screen. Leave this slide up or printed.

## Slide 11

- What we build: a support triage team
- triage_router
- Customer message in. Routes only, never answers.
- billing_agent
- lookup_customer, check_invoice
- technical_agent
- search_kb
- escalation_agent
- create_ticket
- customers.json · kb.json
- tickets.jsonl

**Speaker notes:** Walk top to bottom. The router's description-driven routing is the interesting ADK part: each specialist's description is the routing rule. technical_agent can hand off to escalation_agent when nothing matches. Everything on this slide runs on localhost; no network calls from tools.

## Slide 12

- ADK in five ideas
- An agent is a name, a model and an instruction
- A tool is a plain Python function
- sub_agents turns agents into a team
- The package must expose root_agent
- adk web serves a chat UI and a trace
- root_agent = Agent(
-   name="triage_router",
-   model="gemini-3.5-flash-lite",
-   instruction="Do not answer.",
-   sub_agents=[billing_agent,
-     technical_agent,
-     escalation_agent],
- )
- Run adk web from the folder that contains support_triage/, then open localhost:8000.

**Speaker notes:** Ten-minute demo. Open the reference solution in an editor and run it. Stress that a tool's docstring is what the model reads, and each sub-agent's description is its routing rule. Show the trace panel; participants will rely on it in Lab 4. The model name is read from the WORKSHOP_MODEL environment variable in the kit; confirm the current free-tier model before the event.

## Slide 13

- 02
- Five timed labs
- From a blank folder to a reviewed, running app

## Slide 14

- 0:18 · 15 min · /elephant-grow
- Lab 1: Design with no code
- Settle five things
- PROMPT
- /elephant-grow I want a local-only support triage system in Google ADK. A router sends each message to billing, technical or escalation. Ask at most 5 questions at a time and challenge my assumptions.
- Which messages go where
- Tool inputs, outputs, errors
- Severity rules for tickets
- What is out of scope
- Three messages, three routes
- Hard stop 0:33. The skill refuses to write code. That is the feature.

**Speaker notes:** The full prompt is in the lab guide; this is the short form. Circulate. If anyone is writing code, stop them. Remind people the five bullets are what they carry into Lab 2. Anyone unfinished at 0:33 moves on with what they have.

## Slide 15

- 0:33 · 10 min · /elephant-teach
- Lab 2: Write the design doc
- Five required sections
- PROMPT
- /elephant-teach Write the design document to docs/DESIGN.md from our discussion.
- Problem
- Technical Plan
- Alternatives
- Detailed Implementation
- Evaluation Criteria
- Check it yourself
- Every file is listed. Every criterion can be checked by a person or a test.
- Open Questions is optional.
- Hard stop 0:43. Stuck? Copy checkpoints/DESIGN.md to docs/DESIGN.md.

**Speaker notes:** Stay in the same session as Lab 1 so the skill has the discussion to draw from. Commit the file afterwards. Highlight the quality bar: Detailed Implementation enumerates every file, and Evaluation Criteria are checkable, not adjectives.

## Slide 16

- 0:43 · 10 min · /goldfish-ready
- Lab 3: The readiness gate
- Use a fresh context
- PROMPT
- /goldfish-ready docs/DESIGN.md
- Open a new terminal tab
- Start a fresh agy session
- Run the gate on your doc
- If Not ready, fix the doc once
- Verdict: Ready or Not ready
- Every gap it lists is a bug you would have found an hour into coding.
- Up front: the facilitator demos /goldfish-understand and /goldfish-critic live.

**Speaker notes:** Run the five-minute demo first on a volunteer's document: goldfish-understand (what it understood, what is missing), then goldfish-critic (findings grouped by severity). Participants run only goldfish-ready to save quota. Do not let anyone use /clear in the old session; a new session is the point.

## Slide 17

- 0:53 · 25 min · /implement-design
- Lab 4: Build it and run it
- Run /implement-design docs/DESIGN.md
- Run the offline tests, no key needed
- Start adk web from the project root
- Send three messages, a few seconds apart
- Open the trace for each
- | Message | Expected route |
- | --- | --- |
- | I was charged twice, my email is maya@example.com | billing_agent, overcharge of 29 |
- | My app crashes when I launch it | technical_agent, crash article |
- | Your whole service is down and we lost data | escalation_agent, ticket id |
- Wrong output? Fix the document first, then re-run. Do not patch in chat. Hard stop 1:18.

**Speaker notes:** This is the longest lab. The spec-driven rule is the lesson: decide whether the document or the code was wrong. If the document, edit it and re-run implement-design. Common snags: adk web started from inside support_triage (no agents listed), 429 from messaging too fast, wrong model name (404). Anyone not running at 1:18 pairs with a neighbour.

## Slide 18

- 1:18 · 10 min · /adversary-review
- Lab 5: Hostile review
- In a fresh session
- PROMPT
- /adversary-review support_triage/ tests/
- Run the review on your code and tests
- Fix the two worst findings
- Log the rest under Open Questions
- Numbered findings, then a verdict
- It ends APPROVED or blocked. You will not reach APPROVED in ten minutes. That is fine.
- Working code is not the same as reviewed code.

**Speaker notes:** Ask two or three people to read their top finding aloud. Note which findings the design doc could have prevented, and which only a code review finds. That contrast is the takeaway of the day.

## Slide 19

- 03
- Safety nets and wrap-up
- Checkpoints, homework and what comes next

## Slide 20

- Behind? Use the checkpoint.
- | At | Not done | Do this |
- | --- | --- | --- |
- | 0:33 | Design talk | Go to Lab 2 with your five bullets |
- | 0:43 | No design doc | Copy checkpoints/DESIGN.md to docs/ |
- | 0:53 | No Ready verdict | Carry on; we discuss the gate on screen |
- | 1:18 | App not running | Pair with a neighbour whose app runs |
- Out of free-tier quota? Same rule: take the checkpoint and keep moving.

**Speaker notes:** Nobody waits for stragglers. If someone runs out of Antigravity quota, they use the checkpoint file for that lab and follow along on screen. The reference solution is in the starter kit as an answer key for after the session.

## Slide 21

- Homework
- Run /goldfish-understand and /goldfish-critic on your own doc
- Add a fourth specialist using all seven steps
- Compare your code with the reference solution

**Speaker notes:** Point to the starter kit repo for the reference solution (the answer-key branch) and to the skills repo on GitHub (techpeerPat/elephant-goldfish-skills) for the installation steps and the design document specification.

## Slide 22

- Hands-on workshop
- What did the document catch that the code never would have?

**Speaker notes:** Take answers from two people, then move to the homework.
