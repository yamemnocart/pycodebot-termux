import requests
from core.exceptions import GitHubRateLimitError, NetworkTimeoutError, SearchError

class GitHubSearch:
    API_SEARCH = "https://api.github.com/search/issues"
    API_CODE = "https://api.github.com/search/code"

    def __init__(self, config):
        self.cfg = config
        self.token = config.get("github_token", "").strip()
        self.weight = 7  # Trọng số cao sau Stack Overflow

    def _headers(self):
        h = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _check_limit(self, resp):
        """Tự động phát hiện hết lượt gọi API"""
        remaining = resp.headers.get("X-RateLimit-Remaining", "9999")
        if resp.status_code == 403 and remaining == "0":
            reset = int(resp.headers.get("X-RateLimit-Reset", 0))
            raise GitHubRateLimitError(
                f"GitHub hết lượt gọi (60/giờ không Token / 5000 có Token). "
                f"Reset sau {max(0, (reset - __import__('time').time())//60)} phút. "
                f"Thêm Token vào ~/.pycodebot/config.json để nâng cấp."
            )

    def search_code_and_issues(self, query: str, limit: int = 3) -> list:
        """Tìm đồng thời trong Issues (đã giải quyết) + Code snippets"""
        results = []
        q = f"{query} is:issue is:closed language:python"

        try:
            # Bước 1: Tìm Issues đóng (thường có giải pháp)
            r = requests.get(
                self.API_SEARCH,
                params={"q": q, "per_page": limit, "sort": "comments"},
                headers=self._headers(),
                timeout=self.cfg["timeout_request"]
            )
            self._check_limit(r)
            r.raise_for_status()
            data = r.json()

            for item in data.get("items", [])[:limit]:
                body = (item.get("body") or "")[:2000]
                # Trích xuất code block markdown ```python ... ```
                codes = []
                import re
                for m in re.findall(r"```python\n(.*?)```", body, re.S):
                    codes.append(m.strip()[:800])
                # Loại bỏ code khỏi nội dung text
                clean = re.sub(r"```.*?```", "", body, flags=re.S).strip()
                results.append({
                    "content": clean or item["title"],
                    "vote": item.get("comments", 0),  # Dùng số bình luận thay vote
                    "code": codes[:1],
                    "source": f"GitHub Issue #{item['number']} · {item['repository_url'].split('/')[-1]}",
                    "weight": self.weight
                })

        except GitHubRateLimitError:
            raise  # Truyền lên để Engine hiển thị người dùng
        except requests.exceptions.Timeout:
            raise NetworkTimeoutError("GitHub API timeout")
        except Exception:
            pass  # GitHub lỗi → bỏ qua, không làm chết bot

        return results
