from bs4 import BeautifulSoup
from .base import BaseScraper

class StackOverflowScraper(BaseScraper):
    weight = 10  # Trọng số cao nhất

    def extract(self, url: str) -> dict:
        html = self._fetch(url)
        soup = BeautifulSoup(html, "lxml")
        answers = soup.select("div.answer")
        if not answers:
            return None
        # Lấy top 3 vote cao nhất rồi chọn #1
        scored = []
        for ans in answers[:3]:
            try:
                vote = int(ans["data-score"])
            except Exception:
                vote = 0
            body = ans.select_one("div.s-prose")
            if not body:
                continue
            # Tách code ra riêng
            code_blocks = [c.get_text(strip=True) for c in body.select("pre code")]
            # Loại bỏ code khỏi văn bản giải thích
            for tag in body.select("pre, code"):
                tag.decompose()
            text = body.get_text("\n", strip=True)
            scored.append((vote, text, code_blocks))
        if not scored:
            return None
        scored.sort(reverse=True, key=lambda x: x[0])
        best_vote, best_text, codes = scored[0]
        return {
            "content": best_text,
            "vote": best_vote,
            "code": codes[:1],  # Chỉ lấy code đầu tiên
            "source": f"Stack Overflow (+{best_vote})",
            "weight": self.weight
        }
