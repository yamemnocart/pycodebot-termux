from bs4 import BeautifulSoup
from .base import BaseScraper

class GFGScraper(BaseScraper):
    weight = 4  # Dễ hiểu, trung bình

    def extract(self, url: str) -> dict:
        html = self._fetch(url)
        soup = BeautifulSoup(html, "lxml")

        # Loại bỏ quảng cáo, related posts
        for bad in soup.select(".ads, .code-block, .recommendedPosts, .sidebar"):
            bad.decompose()

        article = soup.select_one("article, .article--viewer_content, .entry-content")
        if not article:
            return None

        # Tách code
        codes = []
        for pre in article.select("pre, div.code-container"):
            codes.append(pre.get_text(strip=True)[:800])
            pre.decompose()

        text = article.get_text("\n", strip=True)
        # Giữ 3 đoạn đầu tiên, tổng <1500 ký tự (nhẹ RAM)
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        short = "\n".join(paragraphs[:3])[:1500]

        return {
            "content": short,
            "vote": 2,  # GFG không có vote → cho điểm mặc định thấp
            "code": codes[:1],
            "source": "GeeksforGeeks",
            "weight": self.weight
        }
