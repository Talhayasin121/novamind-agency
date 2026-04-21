from fastapi import FastAPI, BackgroundTasks, Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="NovaMind Agents API")

# Simple API Key Security
API_KEY = os.getenv("AGENT_API_KEY", "dev-secret-key-123")
api_key_header = APIKeyHeader(name="X-Agent-Secret-Key", auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

class TaskPayload(BaseModel):
    task_id: str
    from_agent: str
    to_agent: str
    task_type: str
    priority: str = "normal"
    input: Dict[str, Any]
    deadline: str | None = None
    status: str = "pending"

def dummy_background_worker(payload: TaskPayload):
    # This will be replaced by actual agent routing logic in Phase 2
    print(f"Processing task {payload.task_id} for {payload.to_agent}")

@app.post("/run", status_code=202)
async def run_agent(
    payload: TaskPayload, 
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    """
    Webhook endpoint for n8n to trigger agents.
    Returns 202 Accepted immediately to prevent n8n timeouts,
    and runs the actual agent logic in the background.
    """
    background_tasks.add_task(dummy_background_worker, payload)
    return {"status": "accepted", "task_id": payload.task_id, "message": "Task queued for processing in background"}

@app.get("/health")
def health_check():
    return {"status": "ok"}