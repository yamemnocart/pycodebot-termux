# 🐍 PyCodeBot Termux v1.0
> **Bot trả lời câu hỏi lập trình Python chạy trực tiếp trên Termux (Android)**  
> Không cần API Key trả phí, không cần máy chủ, tối ưu cho điện thoại **RAM ≤ 4GB**, phản hồi **< 3 giây**.

---

## ✨ TÍNH NĂNG CHÍNH
- 🔍 **Tìm kiếm thông minh**: DuckDuckGo miễn phí + GitHub API (Issues/Gists/Code)
- 🕷️ **5 scraper chuyên biệt**: Stack Overflow (ưu tiên #1), GitHub, GeeksforGeeks, Real Python, TutorialsPoint + 1 scraper đa năng dự phòng mọi trang web
- 🧠 **Bộ não tự xử lý**:
  - Lọc trùng lặp nội dung > 70% bằng thuật toán **MinHash 32** (siêu nhẹ)
  - Xếp hạng câu trả lời theo `điểm vote × trọng số nguồn uy tín`
  - **Tự dịch sang tiếng Việt**, giữ nguyên 100% tên hàm, thư viện, code
  - ✅ **Chạy code mẫu an toàn** trong sandbox 3 giây, báo lỗi nếu có
- ⚡ **Tối ưu tốc độ**: Cache 7 ngày → hỏi lại câu cũ trả về trong 0.1s
- 💬 **Giao diện chat đơn giản**: `[Bạn]: ...` `[Bot]: ...`
- 📜 **Lịch sử 50 câu hỏi**, 5 lệnh hỗ trợ: `/help /clear /history /cache /exit`
- 🛡️ **Chống chặn IP**: User-Agent xoay vòng 24 bản, delay ngẫu nhiên, tự động backoff khi gặp lỗi 429

---

## ⚙️ YÊU CẦU HỆ THỐNG
- Android 7.0+
- Termux (tải từ F-Droid, KHÔNG dùng bản CH Play đã lỗi thời)
- RAM ≥ 2GB (tối ưu nhất ≤ 4GB)
- Kết nối mạng Wi-Fi / 4G

---

## 🚀 CÀI ĐẶT 1 DÒNG LỆNH
Mở Termux, **dán toàn bộ dòng dưới đây và nhấn Enter**:
```bash
pkg update -y && pkg upgrade -y && \
pkg install -y python git libxml2 libxslt libcrypt ndk-sysroot clang && \
git clone https://github.com/pycodebot/termux-bot.git pycodebot && \
cd pycodebot && \
pip install --upgrade pip && \
pip install -r requirements.txt
