from flask import Flask, render_template, request, jsonify
import requests
import json
import markdown
import bleach
import html

app = Flask(__name__)

# Set the address of the Server.
server_url = 'http://127.0.0.1:8080/v1/chat/completions'
# Set whether to enable streaming mode.
is_streaming = True

# Set the default model
default_model = 'gemma-3-1b-it-rk3588-w8a8-opt-1-hybrid-ratio-0.0.rkllm'

# Create a session object.
session = requests.Session()
session.keep_alive = False  # Close the connection pool to maintain a long connection.
adapter = requests.adapters.HTTPAdapter(max_retries=5)
session.mount('https://', adapter)
session.mount('http://', adapter)

# Define allowed HTML tags and attributes for sanitization
ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + ['p', 'div', 'span', 'br', 'hr', 'pre', 'code', 
                                                     'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                                                     'ul', 'ol', 'li', 'blockquote', 'em', 'strong',
                                                     'table', 'thead', 'tbody', 'tr', 'th', 'td']

ALLOWED_ATTRIBUTES = dict(bleach.sanitizer.ALLOWED_ATTRIBUTES)
ALLOWED_ATTRIBUTES.update({
    'code': ['class'],
    'pre': ['class'],
    'span': ['class', 'style'],
    'div': ['class', 'style'],
    'p': ['class', 'style'],
    'a': ['href', 'title', 'target'],
})

def format_markdown(text):
    """
    Convert markdown text to HTML with proper handling of special characters
    """
    # Process markdown manually for common patterns
    # Handle bold text (** **)
    text = text.replace('**', '<strong>', 1)
    while '**' in text:
        text = text.replace('**', '</strong>', 1)
        if '**' in text:
            text = text.replace('**', '<strong>', 1)
    
    # Handle italic text (* *)
    text = text.replace('*', '<em>', 1)
    while '*' in text:
        text = text.replace('*', '</em>', 1)
        if '*' in text:
            text = text.replace('*', '<em>', 1)
    
    # Handle line breaks
    text = text.replace('\n', '<br>\n')
    
    # Handle bullet points
    lines = text.split('<br>\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('* '):
            lines[i] = '<li>' + line.strip()[2:] + '</li>'
    
    # If we have list items, wrap them in a ul
    has_list = any(line.startswith('<li>') for line in lines)
    if has_list:
        in_list = False
        for i, line in enumerate(lines):
            if line.startswith('<li>') and not in_list:
                lines[i] = '<ul>' + line
                in_list = True
            elif not line.startswith('<li>') and in_list:
                lines[i-1] = lines[i-1] + '</ul>'
                in_list = False
        if in_list:
            lines[-1] = lines[-1] + '</ul>'
    
    text = '<br>\n'.join(lines)
    
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    if user_message == "exit":
        return jsonify({"response": "The RKLLM Server is stopping......", "html": "<p>The RKLLM Server is stopping......</p>"})
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'not_required'
    }

    data = {
        "model": default_model,
        "messages": [{"role": "user", "content": user_message}],
        "stream": is_streaming
    }

    try:
        responses = session.post(server_url, json=data, headers=headers, stream=is_streaming, verify=False, timeout=60)

        if not is_streaming:
            if responses.status_code == 200:
                response_data = json.loads(responses.text)
                response_text = response_data["choices"][-1]["message"]["content"]
                html_response = format_markdown(response_text)
                return jsonify({"response": response_text, "html": html_response})
            else:
                return jsonify({"error": responses.text}), 500
        else:
            if responses.status_code == 200:
                response_text = ""
                for line in responses.iter_lines():
                    if line:
                        try:
                            line_text = line.decode('utf-8')
                            if line_text.startswith("data: "):
                                if line_text == "data: [DONE]":
                                    continue
                                line_json = json.loads(line_text.split("data: ")[1])
                                if "choices" in line_json and len(line_json["choices"]) > 0:
                                    if "delta" in line_json["choices"][-1] and "content" in line_json["choices"][-1]["delta"]:
                                        response_text += line_json["choices"][-1]["delta"]["content"]
                        except Exception as e:
                            print(f"Error processing line: {e}")
                            continue
                
                html_response = format_markdown(response_text)
                return jsonify({"response": response_text, "html": html_response})
            else:
                return jsonify({"error": responses.text}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON response from server"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
