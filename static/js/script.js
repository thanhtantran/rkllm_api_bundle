document.addEventListener('DOMContentLoaded', function() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');
    const modelSelect = document.getElementById('model-select');

    // Load available models
    loadModels();

    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });

    // Focus on input when page loads
    userInput.focus();

    function loadModels() {
        fetch('/models')
            .then(response => response.json())
            .then(data => {
                modelSelect.innerHTML = '';
                if (data.data && data.data.length > 0) {
                    data.data.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model.id;
                        option.textContent = model.id;
                        modelSelect.appendChild(option);
                    });
                } else {
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'No models available';
                    modelSelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Error loading models:', error);
                modelSelect.innerHTML = '<option value="">Error loading models</option>';
            });
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        const selectedModel = modelSelect.value;
        if (!selectedModel) {
            addMessage('Please select a model first.', 'error');
            return;
        }

        // Disable button and show loading state
        sendBtn.disabled = true;
        sendBtn.textContent = 'Sending...';

        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                model: selectedModel
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Add bot message to chat
            if (data.html) {
                addMessage(data.html, 'bot', true);
            } else {
                addMessage(data.response, 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Failed to get response. Please try again.', 'error');
        })
        .finally(() => {
            // Re-enable button
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send';
        });
    }

    function addMessage(content, sender, isHtml = false) {
        // Create message container
        const messageContainer = document.createElement('div');
        messageContainer.className = `message-container ${sender}-message-container`;
        
        // Create sender label
        const senderLabel = document.createElement('div');
        senderLabel.className = `sender-name ${sender}-sender`;
        senderLabel.textContent = sender === 'user' ? 'You' : 'RKLLM';
        
        // Create message bubble
        const messageBubble = document.createElement('div');
        messageBubble.className = `message ${sender}-message`;
        
        // Set content
        if (isHtml) {
            messageBubble.innerHTML = content;
        } else {
            // Basic formatting for non-HTML content
            const formattedText = content
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>');
            messageBubble.innerHTML = formattedText;
        }
        
        // Add to DOM
        messageContainer.appendChild(messageBubble);
        chatLog.appendChild(senderLabel);
        chatLog.appendChild(messageContainer);
        
        // Scroll to bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    }
});
