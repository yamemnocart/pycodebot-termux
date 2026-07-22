import json
import os
import time
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

class Cache:
    def __init__(self, config):
        self.dir = Path.home() / ".pycodebot" / "cache"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.days = config["cache_days"]

    def _path(self, key: str) -> Path:
        return self.dir / f"{key}.json"

    def get(self, key: str):
        p = self._path(key)
        if not p.exists():
            return None
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if time.time() - data["ts"] > self.days * 86400:
                p.unlink(missing_ok=True)
                return None
            return data["answer"]
        except Exception:
            p.unlink(missing_ok=True)
            return None

    def set(self, key: str, answer: str):
        p = self._path(key)
        payload = json.dumps({"ts": time.time(), "answer": answer}, ensure_ascii=False)
        # Ghi nguyên tử: file tạm → đổi tên
        fd, tmp = tempfile.mkstemp(dir=str(self.dir), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(payload)
            os.replace(tmp, p)
        except Exception:
            try: os.unlink(tmp)
            except: pass
