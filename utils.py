import re
import os

def apply_chat_template(messages, model_path=None):
    """
    A flexible chat template function that supports various models.
    The format is determined by the model name set in the global_model variable.
    """
    # Avoid circular import by not importing global_model directly
    # Instead, use the model_path parameter if provided
    if model_path is None:
        # Default to DeepSeek format if no model path is provided
        begin_of_sentence = "<｜begin of sentence｜>"
        end_of_sentence = "<｜end of sentence｜>"
        user_position = "<｜User｜>"
        assistant_position = "<｜Assistant｜>"
        think_content = re.compile('<think>.*</think>')

        sentence = ""
        sentence += begin_of_sentence
        for msg in messages:
            if msg['role'] == 'system':
                sentence += msg['content']
            if msg['role'] == 'user':
                sentence += user_position
                sentence += msg['content']
            if msg['role'] == "assistant":
                sentence += assistant_position
                sentence += msg['content']
                sentence += end_of_sentence

        sentence = think_content.sub('', sentence)
        return sentence
    
    # If model_path is provided, determine the model type
    model_name = os.path.basename(model_path).lower()
    
    # DeepSeek models
    if any(name in model_name for name in ["deepseek", "qwen"]):
        begin_of_sentence = "<｜begin of sentence｜>"
        end_of_sentence = "<｜end of sentence｜>"
        user_position = "<｜User｜>"
        assistant_position = "<｜Assistant｜>"
        think_content = re.compile('<think>.*</think>')

        sentence = ""
        sentence += begin_of_sentence
        for msg in messages:
            if msg['role'] == 'system':
                sentence += msg['content']
            if msg['role'] == 'user':
                sentence += user_position
                sentence += msg['content']
            if msg['role'] == "assistant":
                sentence += assistant_position
                sentence += msg['content']
                sentence += end_of_sentence

        sentence = think_content.sub('', sentence)
        return sentence
    
    # Gemma models
    elif "gemma" in model_name:
        conversation = ""
        for msg in messages:
            if msg['role'] == 'system':
                conversation += f"<start_of_turn>system\n{msg['content']}<end_of_turn>\n"
            elif msg['role'] == 'user':
                conversation += f"<start_of_turn>user\n{msg['content']}<end_of_turn>\n"
            elif msg['role'] == "assistant":
                conversation += f"<start_of_turn>model\n{msg['content']}<end_of_turn>\n"
        
        # Add the final assistant turn prompt
        conversation += "<start_of_turn>model\n"
        return conversation
    
    # Llama models
    elif any(name in model_name for name in ["llama", "mistral"]):
        conversation = ""
        for msg in messages:
            if msg['role'] == 'system':
                conversation += f"<s>[INST] <<SYS>>\n{msg['content']}\n<</SYS>>\n\n"
            elif msg['role'] == 'user':
                if conversation:
                    conversation += f"{msg['content']} [/INST]"
                else:
                    conversation += f"<s>[INST] {msg['content']} [/INST]"
            elif msg['role'] == "assistant":
                conversation += f" {msg['content']}</s>"
                if msg != messages[-1]:  # If not the last message
                    conversation += f"<s>[INST] "
        
        return conversation
    
    # Phi models
    elif "phi" in model_name:
        conversation = ""
        for msg in messages:
            if msg['role'] == 'system':
                conversation += f"<|system|>\n{msg['content']}\n"
            elif msg['role'] == 'user':
                conversation += f"<|user|>\n{msg['content']}\n"
            elif msg['role'] == "assistant":
                conversation += f"<|assistant|>\n{msg['content']}\n"
        
        # Add the final assistant prompt
        if messages and messages[-1]['role'] != 'assistant':
            conversation += "<|assistant|>\n"
        
        return conversation
    
    # Baichuan models
    elif "baichuan" in model_name:
        conversation = ""
        for msg in messages:
            if msg['role'] == 'system':
                conversation += f"<reserved_106>{msg['content']}"
            elif msg['role'] == 'user':
                conversation += f"<reserved_107>{msg['content']}"
            elif msg['role'] == "assistant":
                conversation += f"<reserved_108>{msg['content']}"
        
        # Add the final assistant prompt
        if messages and messages[-1]['role'] != 'assistant':
            conversation += "<reserved_108>"
        
        return conversation
    
    # Default format (ChatML-like) for other models
    else:
        conversation = ""
        for msg in messages:
            if msg['role'] == 'system':
                conversation += f"<s>[INST] <<SYS>>\n{msg['content']}\n<</SYS>>\n\n"
            elif msg['role'] == 'user':
                if conversation:
                    conversation += f"{msg['content']} [/INST]"
                else:
                    conversation += f"<s>[INST] {msg['content']} [/INST]"
            elif msg['role'] == "assistant":
                conversation += f" {msg['content']}</s>"
                if msg != messages[-1]:  # If not the last message
                    conversation += f"<s>[INST] "
        
        return conversation