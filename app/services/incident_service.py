incidents = {}


def save_incident(incident_id: str, incident_data: dict):
    incidents[incident_id] = incident_data


def get_incident(incident_id: str):
    return incidents.get(incident_id)