import random
import time
import requests
from core.exceptions import ScrapeError, NetworkTimeoutError

class BaseScraper:
    def __init__(self, config):
        self.cfg = config
        self.session = requests.Session()
        self.weight = 1  # Trọng số nguồn mặc định

    def _headers(self):
        return {
            "User-Agent": random.choice(self.cfg["user_agents"]),
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate"
        }

    def _fetch(self, url: str) -> str:
        delay = random.uniform(0.3, 1.2)
        time.sleep(delay)  # Chống chặn IP
        try:
            r = self.session.get(
                url, headers=self._headers(),
                timeout=self.cfg["timeout_request"],
                stream=True
            )
            # Giới hạn kích thước trang <800KB để tiết kiệm RAM
            size = 0
            chunks = []
            for chunk in r.iter_content(8192, decode_unicode=True):
                size += len(chunk)
                chunks.append(chunk)
                if size > 800 * 1024:
                    break
            r.close()
            return "".join(chunks)
        except requests.exceptions.Timeout:
            raise NetworkTimeoutError(f"Timeout: {url[:60]}")
        except Exception as e:
            raise ScrapeError(f"{e.__class__.__name__}: {url[:60]}")

    def extract(self, url: str) -> dict:
        raise NotImplementedError
