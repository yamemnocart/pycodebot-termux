import time
import hashlib
from .exceptions import *
from search.duckduckgo import DuckDuckGoSearch
from search.github_search import GitHubSearch
from scrapers.stackoverflow import StackOverflowScraper
from scrapers.geeksforgeeks import GFGScraper
from scrapers.tutorialspoint import TPScraper
from scrapers.realpython import RPScraper
from scrapers.generic import GenericScraper
from synthesizer.ranker import Ranker
from synthesizer.deduplicator import Deduplicator
from synthesizer.translator import Translator
from synthesizer.code_sandbox import CodeSandbox
from storage.cache import Cache
from storage.history import History

SCRAPER_MAP = [
    ("stackoverflow.com", StackOverflowScraper),
    ("geeksforgeeks.org", GFGScraper),
    ("tutorialspoint.com", TPScraper),
    ("realpython.com", RPScraper),
]

class Engine:
    def __init__(self, config):
        self.cfg = config
        self.cache = Cache(config)
        self.history = History()
        self.ddg = DuckDuckGoSearch(config)
        self.gh = GitHubSearch(config)
        self.dedup = Deduplicator(threshold=0.7)
        self.ranker = Ranker()
        self.translator = Translator()
        self.sandbox = CodeSandbox(timeout=3)

    def _make_cache_key(self, q: str) -> str:
        return hashlib.md5(q.strip().lower().encode()).hexdigest()

    def _pick_scraper(self, url: str):
        for domain, cls in SCRAPER_MAP:
            if domain in url.lower():
                return cls(self.cfg)
        return GenericScraper(self.cfg)

    def answer(self, question: str) -> str:
        """Hàm chính duy nhất mà CLI gọi"""
        t0 = time.time()
        key = self._make_cache_key(question)

        # Bước 1: Kiểm tra cache → tốc độ <0.1s
        cached = self.cache.get(key)
        if cached:
            return f"{cached}\n\n⚡ [Từ bộ đệm, {(time.time()-t0)*1000:.0f}ms]"

        # Bước 2: Tìm kiếm đa nguồn
        try:
            web_urls = self.ddg.search(question, limit=self.cfg["max_results"])
            gh_results = self.gh.search_code_and_issues(question, limit=3)
        except NetworkTimeoutError:
            return "❌ Mạng quá yếu hoặc hết thời gian chờ. Vui lòng thử lại."
        except SearchError as e:
            return f"❌ Lỗi tìm kiếm: {e}"

        # Bước 3: Cào tuần tự (tối ưu RAM thấp)
        extracted = []
        for url in web_urls:
            try:
                scraper = self._pick_scraper(url)
                data = scraper.extract(url)
                if data and data.get("content", "").strip():
                    extracted.append(data)
            except Exception:
                continue  # Bỏ lỗi từng trang, không làm chết toàn bộ
        # Thêm kết quả GitHub
        extracted.extend(gh_results)

        if not extracted:
            return "🤔 Không tìm thấy kết quả nào phù hợp. Thử đổi từ khóa nhé."

        # Bước 4: Lọc trùng lặp MinHash
        unique = self.dedup.filter(extracted)

        # Bước 5: Xếp hạng theo vote × trọng số
        ranked = self.ranker.sort(unique)
        best = ranked[0]

        # Bước 6: Dịch sang tiếng Việt
        try:
            vi_text = self.translator.to_vietnamese(best["content"], max_lines=self.cfg["answer_lines"])
        except TranslationError:
            vi_text = best["content"]

        # Bước 7: Kiểm tra code nếu có
        code_note = ""
        if best.get("code"):
            safe = self.sandbox.run(best["code"][:500])  # Giới hạn 500 ký tự
            if safe["error"]:
                code_note = f"\n\n⚠️ Code mẫu chạy báo lỗi: {safe['error'][:80]}"
            else:
                code_note = "\n\n✅ Code mẫu chạy thành công trong thử nghiệm."

        # Bước 8: Lưu cache & lịch sử
        final = f"{vi_text}\n\n📌 Nguồn: {best['source']}{code_note}\n⏱️ {(time.time()-t0):.1f}s"
        self.cache.set(key, final)
        self.history.add(question, final)
        return final
