from bs4 import BeautifulSoup
from .base import BaseScraper

class RPScraper(BaseScraper):
    weight = 5  # Giải thích chuẩn, uy tín cao

    def extract(self, url: str) -> dict:
        html = self._fetch(url)
        soup = BeautifulSoup(html, "lxml")

        article = soup.select_one("article.post, div.article-content")
        if not article:
            return None

        # Loại bỏ TOC, author box
        for bad in article.select(".toc, .author-card, .newsletter"):
            bad.decompose()

        codes = []
        for pre in article.select("div.codehilite pre, pre code"):
            codes.append(pre.get_text(strip=True)[:800])
        for pre in article.select("pre"):
            pre.decompose()

        text = article.get_text("\n", strip=True)
        paragraphs = [p for p in text.split("\n\n") if p.strip()]

        return {
            "content": "\n".join(paragraphs[:4])[:1800],
            "vote": 5,  # RP nội dung tốt → điểm mặc định cao
            "code": codes[:1],
            "source": "Real Python",
            "weight": self.weight
        }
