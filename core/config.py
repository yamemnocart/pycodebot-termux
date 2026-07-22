import json
import os
import shutil
from pathlib import Path
from .exceptions import ConfigError

DEFAULT_CONFIG = {
    "github_token": "",
    "cache_days": 7,
    "max_results": 10,
    "timeout_request": 5,
    "timeout_total": 15,
    "answer_lines": 4,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 Version/17.5 Safari/605.1.15"
    ] * 8  # Mở rộng ra 24 UA
}

class Config:
    def __init__(self, data: dict):
        self.data = {**DEFAULT_CONFIG, **data}
        self._validate()

    @classmethod
    def load(cls) -> "Config":
        base_dir = Path.home() / ".pycodebot"
        base_dir.mkdir(exist_ok=True)
        cfg_path = base_dir / "config.json"
        example = Path(__file__).parent.parent / "config.example.json"

        if not cfg_path.exists():
            # Tự copy mẫu nếu chưa có
            if example.exists():
                shutil.copy(example, cfg_path)
            else:
                cfg_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False))
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # Tự phục hồi file hỏng
            cfg_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False))
            data = DEFAULT_CONFIG.copy()
        return cls(data)

    def _validate(self):
        if not isinstance(self.data["max_results"], int) or self.data["max_results"] < 1:
            raise ConfigError("max_results phải là số ≥ 1")
        if self.data["timeout_request"] < 1:
            self.data["timeout_request"] = 5

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data[key]
