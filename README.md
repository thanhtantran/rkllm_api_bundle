👉 [🇻🇳 Xem bản tiếng Việt](README-VIE.md)

## Introduction

This code has been updated to use with the lib librkllmrt.so version 1.2.0 - It cannot work with the old lib librkllmrt.so version 1.4.1, and the old code also cannot with with version 1.2.0

Please ensure that your RK3588/RK3576 board has RKNPU driver at least 0.9.8
```bash
admin@orangepi5b:~/rkllm_api_bundle$ sudo cat /sys/kernel/debug/rknpu/version
RKNPU driver: v0.9.8
```

This app has 3 functions:

- RKLLM server code compatible with the OpenAI API format, API endpoint port 8080
- CLI client to connect with rkllm server, question and answer in command line
- Web client to connect with rkllm server, port 5000

## Usage

```bash
git clone https://github.com/thanhtantran/rkllm_api_bundle
cd rkllm_api_bundle
```

Add/Update the required dynamic libraries:

```bash
sudo cp lib/*.so /usr/lib
```

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install Python dependencies:

```bash
uv sync
```

Run server

```bash
uv run server.py
```

- By default, the target platform is rk3588, and the model path is models/gemma-3-1b-it-rk3588-w8a8-opt-1-hybrid-ratio-0.0.rkllm, and the listening port is 8080.
This model is free to download in my Hugging Face repo https://huggingface.co/thanhtantran/gemma-3-1b-it-rk3588-1.2.0
- You can manually specify parameters, such as 
```bash
uv run server.py --rkllm_model_path=path/to/model.rkllm --target_platform=rk3588/rk3576 --port=xxxx
```
- You can let the server run on a screen by using command
```bash
screen -S rkllm-server uv run server.py
```

Then, you can access this server through `http://your.ip:8080/v1/chat/completions`
Please note that the server only implemented POST `/v1/chat/completions` and GET `/v1/models`, NOTE all of the functions as OpenAI

You can use CLI client to test:

```bash
admin@orangepi5b:~/rkllm_api_bundle$ uv run client.py
============================
Input your question in the terminal to start a conversation with the RKLLM model...
============================

*Please enter your question:Hello, who are you?
Q: Hello, who are you?
A:
I am an artificial intelligence language model created by Alibaba Cloud. My purpose is to provide assistance and answer your questions to the best of my ability. How may I assist you today?
*Please enter your question:

```

Or you can use run a web interface via port 5000 (http://IP:5000)

```bash
uv run web_client.py
```

## Notes

Due to performance limitations, the server can only process one conversation at a time. If there is an ongoing conversation that has not been completed, the server will not accept any other conversations.

## Model

There are a lot models converted with librkllmrt.so version 1.2.0 in my Hugging Face repo
https://huggingface.co/thanhtantran

Feel free to download it

## Credits

https://github.com/airockchip/rknn-llm
