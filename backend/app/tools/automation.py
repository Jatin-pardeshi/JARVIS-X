import sys
import os
import asyncio
import webbrowser
from typing import Dict, Any
from app.tools.base import BaseTool

# Dynamically add the workspace root to sys.path so we can import the user's scripts
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if WORKSPACE_ROOT not in sys.path:
    sys.path.append(WORKSPACE_ROOT)

from scripts.automation.send_action import send_whatsapp, send_gmail

class SystemBrowserTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="system_browser",
            description="Opens a URL in the user's default physical web browser (e.g. Chrome). Use this when the user asks to 'open instagram', 'open youtube', etc. Pass a 'url' parameter.",
            required_permissions=["execute_url"]
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        url = params.get("url")
        if not url:
            return {"status": "error", "message": "Missing 'url' parameter"}
        
        try:
            webbrowser.open(url)
            return {"status": "success", "data": f"Successfully opened {url} in the default browser."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class WhatsAppTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="send_whatsapp",
            description="Sends a WhatsApp message using Playwright automation. Pass 'contact' (name of the person) and 'message' parameters.",
            required_permissions=["execute_url"]
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        contact = params.get("contact")
        message = params.get("message")
        
        if not contact or not message:
            return {"status": "error", "message": "Missing 'contact' or 'message' parameter"}
        
        try:
            # send_whatsapp is async, but this execute method is sync.
            asyncio.run(send_whatsapp(contact, message))
            return {"status": "success", "data": f"WhatsApp message sent to {contact}."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class EmailTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="send_email",
            description="Sends a Gmail email using Playwright automation. Pass 'to_email', 'subject', and 'body' parameters.",
            required_permissions=["execute_url"]
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        to_email = params.get("to_email")
        subject = params.get("subject")
        body = params.get("body")
        
        if not to_email or not subject or not body:
            return {"status": "error", "message": "Missing 'to_email', 'subject', or 'body' parameter"}
        
        try:
            asyncio.run(send_gmail(to_email, subject, body))
            return {"status": "success", "data": f"Email sent to {to_email}."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
