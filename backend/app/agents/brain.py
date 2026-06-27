from typing import TypedDict, Annotated, Sequence, Dict, Any
import json
import requests
from langgraph.graph import StateGraph, END
from app.config import settings
from app.tools.forensics import MetadataExtractorTool
from app.tools.online import WebSearchTool, WebScraperTool
from app.tools.automation import SystemBrowserTool, WhatsAppTool, EmailTool

class AgentState(TypedDict):
    messages: Sequence[Dict[str, Any]]
    next_step: str
    plan: list
    execution_results: list

# Register available modules explicitly inside the local tool engine mapping
TOOL_REGISTRY = {
    "metadata_extractor": MetadataExtractorTool(),
    "web_search": WebSearchTool(),
    "web_scraper": WebScraperTool(),
    "system_browser": SystemBrowserTool(),
    "send_whatsapp": WhatsAppTool(),
    "send_email": EmailTool()
}

import time

def call_gemini_llm(prompt: str, system_message: str = "", json_format: bool = False) -> str:
    """Synchronous orchestration interface wrapper abstraction linking directly onto Google Gemini REST API."""
    api_key = settings.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.DEFAULT_MODEL}:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "system_instruction": {"parts": [{"text": system_message}]},
        "contents": [{"parts": [{"text": f"User Action: {prompt}"}]}]
    }
    
    if json_format:
        data["generationConfig"] = {"responseMimeType": "application/json"}
        
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code in [503, 429]:
                print(f"Gemini API rate limit / 503. Retrying {attempt + 1}/{max_retries}...")
                time.sleep(2 ** attempt)
                continue
            return f"Gemini API operational exception: Status code {response.status_code} - {response.text}"
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Failed to contact local intelligence brain engine: {str(e)}"
            time.sleep(2 ** attempt)
    return "Gemini API operational exception: Max retries exceeded due to high demand."

def planner_node(state: AgentState):
    """Parses strategic intents out of standard text input streams into an explicit execution pipeline roadmap array."""
    latest_message = state['messages'][-1]['content']
    
    system_instruction = (
        "You are the JARVIS-X task decomposition agent. Given an objective, output a JSON structure containing an ordered 'plan' array.\n"
        "Each item in the array MUST contain 'tool' and 'parameters' keys.\n"
        "Available tools:\n"
        "1. 'web_search' - requires 'query'\n"
        "2. 'web_scraper' - requires 'url'\n"
        "3. 'metadata_extractor' - requires 'file_path'\n"
        "4. 'system_browser' - requires 'url'. ONLY use this if the user asks to OPEN or VISIT a website (e.g. 'open instagram'). DO NOT use this to send messages.\n"
        "5. 'send_whatsapp' - requires 'contact' and 'message'. Use this anytime the user asks to SEND a whatsapp message.\n"
        "6. 'send_email' - requires 'to_email', 'subject', and 'body'. Use this anytime the user asks to SEND an email.\n"
        "CRITICAL: You must output a JSON object exactly like this:\n"
        "{\n"
        "  \"plan\": [\n"
        "    {\"tool\": \"send_whatsapp\", \"parameters\": {\"contact\": \"jatin\", \"message\": \"hello\"}}\n"
        "  ]\n"
        "}"
    )
    
    llm_output = call_gemini_llm(latest_message, system_instruction, json_format=True)
    
    try:
        parsed_json = json.loads(llm_output)
        plan = parsed_json.get("plan", [])
    except Exception:
        # If parsing fails (e.g., due to an API error string), pass the error directly to the executor
        plan = [{"tool": "api_error", "parameters": {"message": llm_output}}]

    return {"plan": plan, "next_step": "executor"}

def executor_node(state: AgentState):
    """Loops over sequentially mapped operations, checks execution criteria context, and logs operational telemetry."""
    plan = state.get("plan", [])
    results = state.get("execution_results", [])
    
    for milestone in plan:
        tool_name = milestone.get("tool")
        params = milestone.get("parameters", {})
        
        try:
            if tool_name in TOOL_REGISTRY:
                tool_obj = TOOL_REGISTRY[tool_name]
                outcome = tool_obj.execute(params)
                results.append({"tool": tool_name, "result": outcome})
            else:
                results.append({"tool": tool_name, "status": "error", "message": f"Unknown target module tool: {tool_name}"})
        except Exception as e:
            results.append({"tool": tool_name, "status": "error", "message": f"Execution crashed: {str(e)}"})

    return {"execution_results": results, "next_step": "reporter"}

def reporter_node(state: AgentState):
    """Consolidates complex contextual tool performance profiles into a structured markdown executive brief output."""
    raw_results = json.dumps(state.get("execution_results", []))
    latest_message = state['messages'][-1]['content']
    
    prompt = f"User said: {latest_message}\n\nTool execution results:\n{raw_results}\n\nFormulate a helpful and intelligent response to the user based on the results. If the results are empty, just respond directly to the user naturally."
    
    summary = call_gemini_llm(prompt, "You are J.A.R.V.I.S., a highly advanced AI assistant created by Tony Stark. You are witty, concise, and incredibly intelligent.")
    
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