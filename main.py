#!/usr/bin/env python3
"""PyCodeBot Termux - Bot trả lời câu hỏi code từ web | Tối ưu RAM ≤4GB"""
import sys
import os

# Thêm thư mục gốc vào PATH để import mọi module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.engine import Engine
from cli.interface import CLI

def main():
    # 1. Nạp cấu hình, tự tạo nếu thiếu
    config = Config.load()
    
    # 2. Khởi tạo bộ não Engine
    engine = Engine(config)
    
    # 3. Khởi động giao diện CLI kiểu chat
    cli = CLI(engine)
    cli.start_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot đã dừng an toàn. Hẹn gặp lại!")
        sys.exit(0)
