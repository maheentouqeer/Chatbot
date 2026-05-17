import os
import gradio as gr
from groq import Groq

# 🔐 Get API key from Hugging Face secret
GROQ_API_KEY = os.environ.get("apikey")

# ✅ Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# ✅ Conversation history
chat_history = []

# ✅ Chat function
def chat_with_groq(user_input, history_ui):
    if not user_input.strip():
        return "", history_ui

    chat_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            messages=chat_history,
            model="llama3-70b-8192"
        )
        bot_reply = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": bot_reply})
        history_ui.append((user_input, bot_reply))
        return "", history_ui

    except Exception as e:
        error_message = f"❌ Error: {str(e)}"
        history_ui.append((user_input, error_message))
        return "", history_ui

# ✅ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Groq Chatbot (LLaMA 3.3 70B)\nAsk me anything!")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="💬 Your Message", placeholder="Type here and press Enter...")
    clear = gr.Button("🧹 Clear Chat")

    msg.submit(chat_with_groq, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: ([], []), None, [chatbot])

demo.launch()
