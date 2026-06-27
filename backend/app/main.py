from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ScanRequest, ProcessResponse
from app.agents.brain import agent_orchestrator

app = FastAPI(title="JARVIS-X Core Kernel Backend API")

from fastapi.responses import RedirectResponse

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.post("/api/v1/chat/process", response_model=ProcessResponse)
async def process_intent(payload: ScanRequest):
    try:
        initial_state = {
            "messages": [{"sender": "user", "content": payload.prompt}],
            "next_step": "planner",
            "plan": [],
            "execution_results": []
        }
        
        final_state = agent_orchestrator.invoke(initial_state)
        assistant_reply = final_state["messages"][-1]["content"]
        
        return ProcessResponse(
            status="completed",
            response=assistant_reply,
            execution_log=final_state.get("execution_results", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph Execution Exception Fault: {str(e)}")

@app.get("/api/v1/health")
async def health_check():
    return {"status": "online", "engine": "JARVIS-X API Kernel Module Layer v1.0.0"}