
from typing import Literal
from pydantic import BaseModel, Field


class IncidentInput(BaseModel):
    incident_id: str = Field(description="Unique incident identifier")
    incident_description: str = Field(description="Description of the incident")
    affected_service: str = Field(description="Name of the affected service")
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Initial incident severity"
    )



class TriageOutput(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    affected_service: str
    incident_summary: str
    investigation_priority: Literal["low", "medium", "high", "urgent"]
    reasoning: str



class LogAnalysisOutput(BaseModel):
    findings: list[str]
    error_patterns: list[str]
    relevant_logs: list[str]
    conclusion: str


class MetricsAnalysisOutput(BaseModel):
    findings: list[str]
    anomalies: list[str]
    affected_metrics: list[str]
    conclusion: str


class RCAOutput(BaseModel):
    root_cause: str
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_evidence: list[str]
    alternative_hypotheses: list[str]
    explanation: str


class RemediationOutput(BaseModel):
    proposed_action: str
    rationale: str
    risk_level: Literal["low", "medium", "high", "critical"]
    expected_outcome: str
    requires_approval: bool = True



class ApprovalDecision(BaseModel):
    approved: bool
    approved_by: str
    reason: str


class VerificationOutput(BaseModel):
    status: Literal["resolved", "partially_resolved", "unresolved", "unknown"]
    evidence: list[str]
    summary: str
