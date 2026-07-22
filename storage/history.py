import json
from pathlib import Path
from collections import deque

MAX_ITEMS = 50  # Giữ 50 cặp hỏi/đáp gần nhất

class History:
    def __init__(self):
        self.path = Path.home() / ".pycodebot" / "history.json"
        self.path.parent.mkdir(exist_ok=True)
        self.data = deque(maxlen=MAX_ITEMS)
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            for item in raw:
                self.data.append((item["q"], item["a"], item.get("ts", 0)))
        except Exception:
            # File hỏng → tạo mới
            self.data.clear()

    def _save(self):
        try:
            raw = [{"q": q, "a": a, "ts": ts} for q, a, ts in self.data]
            self.path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def add(self, question: str, answer: str):
        """Thêm 1 bản ghi mới, tự động ghi đĩa"""
        import time
        self.data.append((question, answer, int(time.time())))
        self._save()

    def last(self, n: int = 10) -> list:
        """Trả về N câu hỏi gần nhất (dùng trong lệnh /history)"""
        items = list(self.data)[-n:]
        items.reverse()  # Mới nhất lên đầu
        return [(q, a) for q, a, _ in items]

    def clear(self):
        self.data.clear()
        self.path.unlink(missing_ok=True)
