from pydantic import BaseModel
from typing import List, Dict, Any

class ScanRequest(BaseModel):
    prompt: str
    session_id: str | None = None

class ProcessResponse(BaseModel):
    status: str
    response: str
    execution_log: List[Dict[str, Any]]