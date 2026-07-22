import re
import requests
from core.exceptions import TranslationError

# Các token KHÔNG được dịch (tên hàm, thư viện, code)
PROTECTED = re.compile(
    r'\b(?:def|class|import|from|return|if|else|for|while|try|except|with|as|lambda|print|'
    r'open|input|int|str|float|list|dict|set|tuple|bool|None|True|False|self|async|await|'
    r'pip|conda|venv|numpy|pandas|requests|bs4|django|flask|fastapi|tensorflow|torch|'
    r'ValueError|TypeError|IndexError|KeyError|AttributeError|ModuleNotFoundError)\b|'
    r'[a-zA-Z_][a-zA-Z0-9_]*\.(?:py|js|java|cpp|c|h|cs)|'
    r'`[^`]+`|\b\w+\(\)'
)

class Translator:
    API = "https://api.mymemory.translated.net/get"

    def _split_sentences(self, text: str, max_lines: int) -> list:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return lines[:max_lines]

    def _protect(self, text: str):
        placeholders = {}
        def repl(m):
            k = f"\x00{len(placeholders)}\x00"
            placeholders[k] = m.group(0)
            return k
        return PROTECTED.sub(repl, text), placeholders

    def _restore(self, text: str, ph: dict) -> str:
        for k, v in ph.items():
            text = text.replace(k, v)
        return text

    def to_vietnamese(self, text: str, max_lines: int = 4) -> str:
        sentences = self._split_sentences(text, max_lines)
        if not sentences:
            return text.strip()
        out = []
        for s in sentences:
            protected, ph = self._protect(s)
            try:
                r = requests.get(self.API, params={
                    "q": protected[:400], "langpair": "en|vi"
                }, timeout=4)
                r.raise_for_status()
                translated = r.json()["responseData"]["translatedText"]
                out.append(self._restore(translated, ph))
            except Exception:
                out.append(s)  # Fallback: giữ nguyên tiếng Anh
        return "\n".join(out).strip()
