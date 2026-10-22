
from typing import TypedDict, Any


class State(TypedDict):
    incident_id: str
    incident_description: str
    severity: str
    affected_service: str
    investigation_priority: str

    logs: list[str]
    metrics: dict[str, Any]
    log_analysis: str
    metrics_analysis: str

    root_cause: str
    root_cause_confidence: float
    evidence: list[str]

    suggested_remediation: str
    remediation_risk: str
    approval_status: str
    remediation_result: str

    verification_status: str
    verification_details: str

    errors: list[str]
