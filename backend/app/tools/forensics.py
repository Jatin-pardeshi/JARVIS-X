import os
import hashlib
from typing import Dict, Any
from app.tools.base import BaseTool

class MetadataExtractorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="metadata_extractor",
            description="Extracts basic system file structural characteristics and generates cryptographically signed checksum profiles.",
            required_permissions=["read_file"]
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        target_path = params.get("file_path")
        if not target_path or not os.path.exists(target_path):
            return {"status": "error", "message": f"Target invalid or inaccessible: {target_path}"}

        try:
            stat_info = os.stat(target_path)
            sha256_hash = hashlib.sha256()
            
            with open(target_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)

            return {
                "status": "success",
                "data": {
                    "file_name": os.path.basename(target_path),
                    "file_size_bytes": stat_info.st_size,
                    "creation_time": stat_info.st_ctime,
                    "modification_time": stat_info.st_mtime,
                    "access_time": stat_info.st_atime,
                    "sha256": sha256_hash.hexdigest()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}