# 🐍 PyCodeBot Termux
> **Bot trả lời câu hỏi Python chạy trực tiếp trên Termux**  
> Tối ưu cho Android • Không cần API trả phí • Dung lượng nhẹ • Phản hồi nhanh

🔗 **Kho dự án**: https://github.com/yamemnocart/pycodebot-termux

---

## ✨ TÍNH NĂNG NỔI BẬT
- 🔍 **Tìm kiếm đa nguồn**: DuckDuckGo miễn phí + GitHub API (Issues/Code/Gists) + Stack Overflow + GeeksforGeeks + Real Python + TutorialsPoint
- 🧠 **Xử lý thông minh**: Lọc trùng lặp, xếp hạng theo độ uy tín & số bình chọn, tự dịch sang tiếng Việt **giữ nguyên thuật ngữ code**
- ✅ **Kiểm tra an toàn**: Chạy thử đoạn code mẫu trong môi trường giới hạn
- ⚡ **Tối ưu hiệu năng**: Bộ đệm 7 ngày, hoạt động mượt trên máy **RAM ≤ 4GB**, thời gian phản hồi dưới 3 giây
- 💬 **Giao diện đơn giản**: Kiểu hội thoại `[Bạn] ↔ [Bot]`, các lệnh nhanh tiện dụng

---

## 📋 YÊU CẦU
- Android 7.0 trở lên
- **Termux tải từ F‑Droid** (không dùng bản cũ trên CH Play)
- Kết nối mạng ổn định

---

## 🚀 CÀI ĐẶT CHỈ 1 DÒNG
Mở Termux, dán toàn bộ lệnh sau:
```bash
pkg update -y && pkg upgrade -y && \
pkg install -y python git libxml2 libxslt clang && \
git clone https://github.com/yamemnocart/pycodebot-termux.git pycodebot && \
cd pycodebot && pip install -r requirements.txt
