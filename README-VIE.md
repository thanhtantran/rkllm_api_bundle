
## Giới thiệu

Code này đã được cập nhật để sử dụng với thư viện `librkllmrt.so` phiên bản 1.2.0 - Nó **không thể hoạt động với thư viện cũ** `librkllmrt.so` phiên bản 1.4.1, và code cũ cũng không thể hoạt động với phiên bản 1.2.0. Hãy chắc chắn bạn đang định dùng phiên bản nào.

Vui lòng đảm bảo rằng bo mạch RK3588/RK3576 của bạn có driver RKNPU ít nhất là phiên bản 0.9.8  
```bash
admin@orangepi5b:~/rkllm_api_bundle$ sudo cat /sys/kernel/debug/rknpu/version
RKNPU driver: v0.9.8
```

Ứng dụng này có 3 chức năng:

- Mã nguồn server RKLLM tương thích với định dạng API của OpenAI, cổng endpoint là 8080  
- Ứng dụng dòng lệnh (CLI) để kết nối với server rkllm, hỏi và trả lời trên dòng lệnh  
- Ứng dụng web để kết nối với server rkllm, cổng 5000  

## Cách sử dụng

```bash
git clone https://github.com/thanhtantran/rkllm_api_bundle
cd rkllm_api_bundle
```

Thêm/Cập nhật các thư viện động cần thiết:

```bash
sudo cp lib/*.so /usr/lib
```

Cài đặt `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Cài đặt các phụ thuộc Python:

```bash
uv sync
```

Chạy server:

```bash
uv run server.py
```

- Mặc định, nền tảng mục tiêu là `rk3588`, đường dẫn mô hình là `models/gemma-3-1b-it-rk3588-w8a8-opt-1-hybrid-ratio-0.0.rkllm`, và cổng lắng nghe là `8080`.  
Mô hình này có thể tải miễn phí tại Hugging Face repo của tôi: https://huggingface.co/thanhtantran/gemma-3-1b-it-rk3588-1.2.0  
- Bạn có thể chỉ định tham số thủ công, ví dụ:  
```bash
uv run server.py --rkllm_model_path=duong/dan/toi/model.rkllm --target_platform=rk3588/rk3576 --port=xxxx
```  
- Bạn có thể để server chạy nền bằng ứng dụng `screen` trên linux bằng lệnh:  
```bash
screen -S rkllm-server uv run server.py
```

Sau đó, bạn có thể truy cập server qua `http://your.ip:8080/v1/chat/completions`  
Lưu ý rằng server chỉ triển khai `POST /v1/chat/completions` và `GET /v1/models`, tương tự như OpenAI.

Bạn có thể dùng client dòng lệnh để kiểm tra:

```bash
admin@orangepi5b:~/rkllm_api_bundle$ uv run client.py
============================
Nhập câu hỏi của bạn trong terminal để bắt đầu cuộc trò chuyện với mô hình RKLLM...
============================

*Please enter your question:Hello, who are you?
Q: Hello, who are you?
A:
I am an artificial intelligence language model created by Alibaba Cloud. My purpose is to provide assistance and answer your questions to the best of my ability. How may I assist you today?
*Please enter your question:
```

Hoặc bạn có thể chạy giao diện web qua cổng 5000 (http://IP:5000)

```bash
uv run web_client.py
```

## Ghi chú

Do hạn chế về hiệu năng, server chỉ có thể xử lý một cuộc trò chuyện tại một thời điểm. Nếu có cuộc trò chuyện đang diễn ra mà chưa hoàn tất, server sẽ không chấp nhận bất kỳ cuộc trò chuyện nào khác.

## Mô hình

Có rất nhiều mô hình đã được chuyển đổi với thư viện `librkllmrt.so` phiên bản 1.2.0 tại Hugging Face repo của tôi:  
https://huggingface.co/thanhtantran  

Bạn có thể tự do tải về.

## Ghi công

https://github.com/airockchip/rknn-llm
