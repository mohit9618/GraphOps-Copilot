
from langchain_groq import ChatGroq

from app.schemas.incident import LogAnalysisOutput
from app.state import State
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
)

structured_llm = llm.with_structured_output(LogAnalysisOutput)


def log_analyst_node(state: State) -> dict:
    logs = state.get("logs", [])

    prompt = f"""
    You are the log analyst for GraphOps Copilot.

    Incident:
    {state.get("incident_description", "Not provided")}

    Affected service:
    {state.get("affected_service", "Unknown")}

    Available logs:
    {logs}

    Analyze only the supplied logs.
    Identify error patterns, relevant log entries, and findings.
    If the logs contain insufficient evidence, explicitly say so.
    Do not invent log entries or claim a root cause without evidence.
    """

    result = structured_llm.invoke(prompt)

    return {
        "log_analysis": result.conclusion,
        "evidence": result.relevant_logs,
    }
