from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Set the address of the Server.
server_url = 'http://127.0.0.1:8080/rkllm_chat/v1/chat/completions'
# Set whether to enable streaming mode.
is_streaming = True

# Create a session object.
session = requests.Session()
session.keep_alive = False  # Close the connection pool to maintain a long connection.
adapter = requests.adapters.HTTPAdapter(max_retries=5)
session.mount('https://', adapter)
session.mount('http://', adapter)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    if user_message == "exit":
        return jsonify({"response": "The RKLLM Server is stopping......"})
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'not_required'
    }

    data = {
        "model": 'your_model_deploy_with_RKLLM_Server',
        "messages": [{"role": "user", "content": user_message}],
        "stream": is_streaming
    }

    responses = session.post(server_url, json=data, headers=headers, stream=is_streaming, verify=False)

    if not is_streaming:
        if responses.status_code == 200:
            response_data = json.loads(responses.text)
            return jsonify({"response": response_data["choices"][-1]["message"]["content"]})
        else:
            return jsonify({"error": responses.text})
    else:
        if responses.status_code == 200:
            response_text = ""
            for line in responses.iter_lines():
                if line:
                    line = json.loads(line.decode('utf-8').split("data: ")[1])
                    response_text += line["choices"][-1]["delta"]["content"]
            return jsonify({"response": response_text})
        else:
            return jsonify({"error": responses.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
