import subprocess
import tempfile
import os
from core.exceptions import SandboxError

class CodeSandbox:
    def __init__(self, timeout: int = 3):
        self.timeout = timeout

    def run(self, code: str) -> dict:
        """Chạy code Python trong môi trường giới hạn, không quyền mạng"""
        if not code.strip():
            return {"output": "", "error": None}
        # Giới hạn: chỉ stdlib, tắt mạng, 3s, 64MB RAM
        wrapper = (
            "import sys, resource\n"
            "resource.setrlimit(resource.RLIMIT_CPU, (%d, %d))\n"
            "resource.setrlimit(resource.RLIMIT_AS, (67108864, 67108864))\n"
            "sys.modules['socket'] = None\n"
            "sys.modules['urllib'] = None\n"
            "sys.modules['requests'] = None\n"
            "try:\n"
            "    exec(%r)\n"
            "except Exception as e:\n"
            "    sys.stderr.write(type(e).__name__ + ': ' + str(e)[:200])\n"
            "    sys.exit(1)\n"
        ) % (self.timeout, self.timeout, code)

        try:
            proc = subprocess.run(
                [sys.executable, "-c", wrapper],
                capture_output=True, text=True, timeout=self.timeout + 1,
                cwd=tempfile.gettempdir(),
                env={"PATH": os.environ.get("PATH", "")}
            )
            return {
                "output": proc.stdout[:300],
                "error": proc.stderr.strip() if proc.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {"output": "", "error": "Chạy quá 3 giây, đã dừng an toàn"}
        except Exception as e:
            return {"output": "", "error": f"Sandbox: {e}"}

import sys  # Thêm import bị thiếu ở trên
