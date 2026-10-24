
from langchain_groq import ChatGroq

from app.schemas.incident import LogAnalysisOutput
from app.state import State
from app.tools.logs import search_logs, get_log_context
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)

structured_llm = llm.with_structured_output(LogAnalysisOutput)


def log_analyst_node(state: State) -> dict:
    logs = state.get("logs", [])

    error_logs = search_logs(logs, keyword="error")
    timeout_logs = search_logs(logs, keyword="timeout")

    relevant_logs = list(dict.fromkeys(error_logs + timeout_logs))

    contextual_logs = []

    for log in relevant_logs:
        contextual_logs.extend(
            get_log_context(logs, log, window=1)
        )

    contextual_logs = list(dict.fromkeys(contextual_logs))

    prompt = f"""
    You are the Log Analyst for GraphOps Copilot.

    Incident: {state.get("incident_description", "Unknown")}
    Affected service: {state.get("affected_service", "Unknown")}

    Matching log entries:
    {relevant_logs}

    Log context:
    {contextual_logs}

    Analyze only the provided logs.
    Identify error patterns and relevant evidence.
    Do not invent log entries or assert an unproven root cause.
    If no useful logs are available, explicitly state that evidence
    is insufficient.
    """

    result = structured_llm.invoke(prompt)

    return {
    "log_analysis": result.conclusion,
    "log_evidence": result.relevant_logs,
    }
