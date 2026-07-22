import sys
import os
from cli.utils import *

HELP_TEXT = """📖 Các lệnh hỗ trợ:
  /help     - Hiển thị trợ giúp này
  /clear    - Xóa màn hình Termux
  /history  - Xem 10 câu hỏi gần nhất
  /cache    - Xóa toàn bộ bộ đệm
  /exit     - Thoát bot
"""

class CLI:
    BANNER = r"""
 ____          ____          _        ____        _   
|  _ \ _   _  / ___|___   __| | ___  | __ )  ___ | |_ 
| |_) | | | || |   / _ \ / _` |/ _ \ |  _ \ / _ \| __|
|  __/| |_| || |__| (_) | (_| |  __/ | |_) | (_) | |_ 
|_|    \__, | \____\___/ \__,_|\___| |____/ \___/ \__|
       |___/   Termux Edition v1.0  |  RAM ≤4GB  <3s
"""

    def __init__(self, engine):
        self.engine = engine

    def _print_banner(self):
        print(color(self.BANNER, CYAN))
        print(color("Nhập câu hỏi code của bạn, gõ /help để xem lệnh\n", MUTED))

    def _handle_cmd(self, cmd: str) -> bool:
        """Trả về True nếu đã xử lý xong lệnh đặc biệt"""
        c = cmd.strip().lower()
        if c == "/help":
            print(color(HELP_TEXT, YELLOW)); return True
        if c == "/clear":
            os.system("clear"); return True
        if c == "/history":
            for i, (q, _) in enumerate(self.engine.history.last(10), 1):
                print(f"  {i:2d}. {q[:70]}{'...' if len(q)>70 else ''}")
            return True
        if c == "/cache":
            import shutil
            shutil.rmtree(self.engine.cache.dir, ignore_errors=True)
            print(color("✅ Đã xóa toàn bộ bộ đệm", GREEN)); return True
        if c == "/exit":
            raise KeyboardInterrupt
        return False

    def start_loop(self):
        self._print_banner()
        while True:
            try:
                q = input(color("[Bạn]: ", BLUE + BOLD)).strip()
            except EOFError:
                break
            if not q:
                continue
            if self._handle_cmd(q):
                continue
            print(color("[Bot]: ", GREEN + BOLD), end="", flush=True)
            try:
                ans = self.engine.answer(q)
                print(ans)
            except Exception as e:
                print(color(f"❌ Lỗi hệ thống: {e}", RED))
            print()
