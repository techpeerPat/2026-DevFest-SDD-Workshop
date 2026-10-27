# Support Triage Multi-Agent System

> Checkpoint design document. Use it only if Lab 1 or Lab 2 stalls (quota, time). It follows the section format that `/elephant-teach` produces.

## Problem

A small support team receives free-text customer messages about three kinds of issue: billing questions, technical problems, and urgent or unclear matters. Today a person reads every message and decides who handles it. We want a local prototype that reads a message, routes it to the right specialist, uses small local data sources to produce a grounded answer, and records a ticket when a human must step in. The prototype runs entirely on one laptop with a free-tier Gemini model and has no deployment target.

## Technical Plan

One coordinator agent, `triage_router`, never answers customers itself. It reads the message and transfers the conversation to one of three specialist agents. `billing_agent` looks up the customer and compares their last invoice with their plan price. `technical_agent` searches a small local knowledge base and quotes the matching article. `escalation_agent` writes a ticket to a local file and returns the ticket id. If `technical_agent` finds no match it transfers to `escalation_agent`. All tools are plain Python functions that read or write files inside the project folder and make no network calls. The system is started with `adk web` and tested by typing messages into the browser chat on localhost.

## Alternatives

A single agent with all four tools was rejected because it hides the routing decision and makes the multi-agent structure, which is the point of the exercise, invisible. A sequential pipeline of agents was rejected because triage is a choice among alternatives, not a fixed sequence. A local Ollama model was rejected for this version because tool-calling quality varies by model and the download is large for a 90-minute session. A real ticketing or billing API was rejected because it needs credentials and a network, which breaks the local-only goal.

## Detailed Implementation

| File | Action | Purpose |
| --- | --- | --- |
| `support_triage/__init__.py` | create | Imports `agent` so ADK discovers `root_agent`. |
| `support_triage/tools.py` | create | Four functions: `lookup_customer`, `check_invoice`, `search_kb`, `create_ticket`. Data is read from `data/` relative to the project root. Tickets are appended to `tickets/tickets.jsonl`. |
| `support_triage/agent.py` | create | Defines three `Agent` specialists and `root_agent` named `triage_router` with `sub_agents`. Model name comes from the `WORKSHOP_MODEL` environment variable, default `gemini-3.5-flash-lite`. |
| `tests/test_tools.py` | create | Offline tests for the four tools. No API key needed. |
| `data/customers.json` | existing | Six customers. C-1001 and C-1005 have invoices above plan price. |
| `data/kb.json` | existing | Four knowledge base articles. |

Tool contracts:

| Tool | Input | Output on success | Output on failure |
| --- | --- | --- | --- |
| `lookup_customer` | customer id or email, case-insensitive | `status: found` plus customer record | `status: not_found` |
| `check_invoice` | customer id | plan price, last invoice, `discrepancy` boolean, `overcharge_amount` | `status: not_found` |
| `search_kb` | free text | up to 3 articles, best first | empty `matches` list |
| `create_ticket` | customer id, summary, severity of `low`, `medium` or `high` | `status: created`, `ticket_id` | `status: error` for any other severity |

## Evaluation Criteria

1. `python -m pytest tests -q` passes with no API key set.
2. `adk web` lists `support_triage` and the trace shows `triage_router` transferring each of these messages to the named agent: "I was charged twice, my email is maya@example.com" to `billing_agent`; "My app crashes when I launch it" to `technical_agent`; "Your whole service is down and we lost data" to `escalation_agent`.
3. For maya@example.com the billing answer states an overcharge of 29.
4. A message with no matching article ends with a new line in `tickets/tickets.jsonl`.
5. No file outside the table above is created, and no tool makes a network call.

## Open Questions

- Should billing ever offer a refund? This version says no and only reports the discrepancy.
- Should customers be verified before account details are shown? Out of scope for this prototype and called out as a known gap.
