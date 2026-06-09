from typing import TypedDict, Annotated, Sequence, Dict, Any
import json
import requests
from langgraph.graph import StateGraph, END
from app.config import settings
from app.tools.forensics import MetadataExtractorTool

class AgentState(TypedDict):
    messages: Sequence[Dict[str, Any]]
    next_step: str
    plan: list
    execution_results: list

# Register available modules explicitly inside the local tool engine mapping
TOOL_REGISTRY = {
    "metadata_extractor": MetadataExtractorTool()
}

def call_local_llm(prompt: str, system_message: str = "") -> str:
    """Synchronous orchestration interface wrapper abstraction linking directly onto running local Ollama runtimes."""
    payload = {
        "model": settings.DEFAULT_MODEL,
        "prompt": f"{system_message}\n\nUser Action: {prompt}",
        "stream": False
    }
    try:
        response = requests.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "")
        return f"Ollama operational mapping exception: Status code {response.status_code}"
    except Exception as e:
        return f"Failed to contact local intelligence brain engine: {str(e)}"

def planner_node(state: AgentState):
    """Parses strategic intents out of standard text input streams into an explicit execution pipeline roadmap array."""
    latest_message = state['messages'][-1]['content']
    
    system_instruction = (
        "You are the JARVIS-X task decomposition agent. Given an objective, output a clean JSON structure containing a ordered 'plan' array. "
        "Each array block contains keys: 'tool' and 'parameters'. Available tools: " + ", ".join(TOOL_REGISTRY.keys())
    )
    
    llm_output = call_local_llm(latest_message, system_instruction)
    
    try:
        parsed_json = json.loads(llm_output)
        plan = parsed_json.get("plan", [])
    except Exception:
        plan = [{"tool": "metadata_extractor", "parameters": {"file_path": latest_message}}]

    return {"plan": plan, "next_step": "executor"}

def executor_node(state: AgentState):
    """Loops over sequentially mapped operations, checks execution criteria context, and logs operational telemetry."""
    plan = state.get("plan", [])
    results = state.get("execution_results", [])
    
    for milestone in plan:
        tool_name = milestone.get("tool")
        params = milestone.get("parameters", {})
        
        if tool_name in TOOL_REGISTRY:
            tool_obj = TOOL_REGISTRY[tool_name]
            outcome = tool_obj.execute(params)
            results.append({"tool": tool_name, "result": outcome})
        else:
            results.append({"tool": tool_name, "status": "error", "message": "Unknown target module tool."})

    return {"execution_results": results, "next_step": "reporter"}

def reporter_node(state: AgentState):
    """Consolidates complex contextual tool performance profiles into a structured markdown executive brief output."""
    raw_results = json.dumps(state.get("execution_results", []))
    prompt = f"Summarize the following investigation results into an actionable analysis brief:\n{raw_results}"
    
    summary = call_local_llm(prompt, "You are a senior digital forensics investigator. Provide clean, factual summaries of findings without speculation.")
    
    return {"messages": state['messages'] + [{"sender": "assistant", "content": summary}], "next_step": END}

def router_conditional(state: AgentState):
    return state.get("next_step", END)

# Building execution graph architecture
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("reporter", reporter_node)

workflow.set_entry_point("planner")
workflow.add_conditional_edges("planner", router_conditional, {"executor": "executor", END: END})
workflow.add_conditional_edges("executor", router_conditional, {"reporter": "reporter", END: END})
workflow.add_conditional_edges("reporter", router_conditional, {END: END})

agent_orchestrator = workflow.compile()