import random
import time
import re
import requests
from bs4 import BeautifulSoup
from core.exceptions import SearchError, NetworkTimeoutError

class DuckDuckGoSearch:
    ENDPOINT = "https://html.duckduckgo.com/html/"

    def __init__(self, config):
        self.cfg = config
        self.session = requests.Session()

    def _headers(self):
        return {
            "User-Agent": random.choice(self.cfg["user_agents"]),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
            "Referer": "https://duckduckgo.com/"
        }

    def search(self, query: str, limit: int = 10) -> list:
        results = []
        payload = {"q": query + " solved example", "b": "", "kl": "wt-wt"}
        backoff = 1
        for attempt in range(3):
            try:
                r = self.session.post(
                    self.ENDPOINT, data=payload,
                    headers=self._headers(),
                    timeout=self.cfg["timeout_request"]
                )
                if r.status_code == 429:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                r.raise_for_status()
                break
            except requests.exceptions.Timeout:
                raise NetworkTimeoutError("DuckDuckGo hết thời gian")
            except requests.exceptions.RequestException as e:
                if attempt == 2:
                    raise SearchError(f"DuckDuckGo lỗi: {e}")
                time.sleep(backoff)
                backoff *= 2
        else:
            raise SearchError("DuckDuckGo chặn yêu cầu, thử lại sau 1 phút")

        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.select("a.result__a")[:limit]:
            href = a.get("href", "")
            # Lọc bỏ quảng cáo & liên kết nội bộ DDG
            if href.startswith("http") and "duckduckgo.com" not in href:
                results.append(href)
        return results
