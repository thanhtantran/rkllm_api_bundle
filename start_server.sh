#!/bin/bash

# Tạo một screen mới với tên "server_screen"
screen -dmS server_screen

# Chạy lệnh 'uv run server.py' trong screen đó
screen -S server_screen -X stuff "uv run server.py\n"

# Thoát khỏi screen và để nó chạy nền
screen -d server_screen

echo "Server đã được khởi động trong screen 'server_screen'."
