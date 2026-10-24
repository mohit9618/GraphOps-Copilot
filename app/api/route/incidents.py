from fastapi import APIRouter, HTTPException

from app.schemas.incident import IncidentInput
from app.services.incident_service import save_incident, get_incident

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post("/")
def create_incident(incident: IncidentInput):
    incident_data = incident.model_dump()

    save_incident(incident.incident_id, incident_data)

    return {
        "message": "Incident received successfully",
        "incident": incident_data
    }


@router.get("/{incident_id}")
def retrieve_incident(incident_id: str):
    incident = get_incident(incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return {
        "incident": incident
    }