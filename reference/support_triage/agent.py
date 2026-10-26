"""Reference solution: a coordinator with three specialist sub-agents."""
import os

from google.adk.agents import Agent

from .tools import check_invoice, create_ticket, lookup_customer, search_kb

MODEL = os.getenv("WORKSHOP_MODEL", "gemini-3.5-flash-lite")

billing_agent = Agent(
    name="billing_agent",
    model=MODEL,
    description="Handles invoice, charge, refund and plan-price questions.",
    instruction=(
        "You resolve billing questions. Look the customer up with lookup_customer, "
        "then call check_invoice. If there is a discrepancy, state the exact overcharge "
        "and say it will be reviewed. If the customer cannot be found, ask for their "
        "customer id or email. Never promise a refund."
    ),
    tools=[lookup_customer, check_invoice],
)

technical_agent = Agent(
    name="technical_agent",
    model=MODEL,
    description="Handles how-to questions, login problems, crashes and integrations.",
    instruction=(
        "You resolve technical questions using search_kb. Quote the matching article "
        "title and steps. If nothing matches, say so and transfer to escalation_agent."
    ),
    tools=[search_kb],
)

escalation_agent = Agent(
    name="escalation_agent",
    model=MODEL,
    description="Creates a ticket for anything urgent, unresolved or outside billing and technical.",
    instruction=(
        "You create tickets with create_ticket. Use severity high for outages, data loss "
        "or security concerns, medium for blocked users, low otherwise. Use customer id "
        "'unknown' if none was given. Reply with the ticket id."
    ),
    tools=[create_ticket],
)

root_agent = Agent(
    name="triage_router",
    model=MODEL,
    description="Routes customer support messages to the right specialist.",
    instruction=(
        "You are a support triage router. Do not answer questions yourself. "
        "Transfer billing and invoice questions to billing_agent, technical and how-to "
        "questions to technical_agent, and urgent or unclear issues to escalation_agent."
    ),
    sub_agents=[billing_agent, technical_agent, escalation_agent],
)
