from bs4 import BeautifulSoup
from .base import BaseScraper

class GenericScraper(BaseScraper):
    weight = 1  # Thấp nhất vì không rõ nguồn

    def extract(self, url: str) -> dict:
        try:
            html = self._fetch(url)
        except Exception:
            return None

        soup = BeautifulSoup(html, "lxml")

        # Bước 1: Xóa toàn bộ thẻ không phải nội dung
        for bad in soup.select(
            "script, style, nav, footer, header, aside, form, "
            "iframe, noscript, svg, .ad, .ads, .advertisement"
        ):
            bad.decompose()

        # Bước 2: Tìm thẻ có nhiều text nhất (thường là bài viết)
        best_tag = None
        best_len = 0
        for tag in soup.find_all(["article", "main", "div", "section"]):
            text_len = len(tag.get_text(strip=True))
            if 200 < text_len < 50000 and text_len > best_len:
                # Đảm bảo không phải thẻ cha bao gồm các thẻ con đã chọn
                if best_tag and best_tag in tag.descendants:
                    continue
                best_len = text_len
                best_tag = tag

        if not best_tag:
            best_tag = soup.body or soup

        # Bước 3: Trích code
        codes = []
        for pre in best_tag.select("pre, code"):
            txt = pre.get_text(strip=True)
            if len(txt) > 30:  # Chỉ lấy đoạn code đủ dài
                codes.append(txt[:800])
        for pre in best_tag.select("pre"):
            pre.decompose()

        text = best_tag.get_text("\n", strip=True)
        # Làm sạch dòng trống liên tiếp
        import re
        text = re.sub(r"\n{3,}", "\n\n", text)
        paragraphs = [p for p in text.split("\n\n") if len(p.strip()) > 20]

        return {
            "content": "\n".join(paragraphs[:3])[:1500],
            "vote": 0,
            "code": codes[:1],
            "source": url.split("/")[2][:30],  # Lấy domain làm nguồn
            "weight": self.weight
        }
