import uuid
from datetime import datetime, timezone
from core.supabase_client import get_supabase

def send_task(from_agent: str, to_agent: str, task_type: str, input_data: dict, priority: str = "normal"):
    """
    Creates a new task in the Supabase tasks table, to be picked up by n8n or polled directly.
    """
    supabase = get_supabase()
    
    task_payload = {
        "id": str(uuid.uuid4()),
        "from_agent": from_agent,
        "to_agent": to_agent,
        "type": task_type,
        "priority": priority,
        "payload": input_data,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    response = supabase.table("tasks").insert(task_payload).execute()
    return response.data
    
def write_alert(agent_id: str, severity: str, message: str):
    """Logs an error to the alerts table."""
    supabase = get_supabase()
    alert_payload = {
        "id": str(uuid.uuid4()),
        "agent_id": agent_id,
        "severity": severity,
        "message": message,
        "resolved": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    return supabase.table("alerts").insert(alert_payload).execute()