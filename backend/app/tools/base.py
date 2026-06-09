import abc
import subprocess
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("jarvis_tools")

class BaseTool(abc.ABC):
    def __init__(self, name: str, description: str, required_permissions: List[str]):
        self.name = name
        self.description = description
        self.required_permissions = required_permissions

    @abc.abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        pass

    protected_binaries = ["rm", "dd", "mkfs", "sh", "bash"]

    def safe_subprocess_run(self, cmd_args: List[str]) -> Dict[str, Any]:
        """
        Executes a binary inside a separate process array securely.
        Guards against shell string injections by disallowing raw shell evaluation.
        """
        if not cmd_args or cmd_args[0] in self.protected_binaries:
            return {"status": "error", "message": "Execution blocked: Unauthorized target binary."}

        try:
            result = subprocess.run(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300
            )
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Process execution timed out."}
        except Exception as e:
            return {"status": "error", "message": f"Execution failure: {str(e)}"}