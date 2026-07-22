from bs4 import BeautifulSoup
from .base import BaseScraper

class TPScraper(BaseScraper):
    weight = 3  # Cơ bản, thấp nhất trong chuyên biệt

    def extract(self, url: str) -> dict:
        html = self._fetch(url)
        soup = BeautifulSoup(html, "lxml")

        content = soup.select_one("div.mu-content, div.tutorial-content, article")
        if not content:
            return None

        # Loại bỏ menu, quảng cáo
        for tag in content.select(".mui-top-box, .ad, nav"):
            tag.decompose()

        codes = []
        for pre in content.select("pre"):
            codes.append(pre.get_text(strip=True)[:800])
            pre.decompose()

        text = content.get_text("\n", strip=True)
        paragraphs = [p for p in text.split("\n\n") if p.strip()]

        return {
            "content": "\n".join(paragraphs[:3])[:1200],
            "vote": 1,
            "code": codes[:1],
            "source": "TutorialsPoint",
            "weight": self.weight
        }
