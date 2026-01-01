"""
Gradio web interface for the Icebreaker Bot
"""

import sys
import uuid
import logging
import gradio as gr

from modules.data_extraction import extract_linkedin_profile
from modules.data_preprocessing import split_profile_data, create_retriever
from modules.query_engine import generate_initial_facts, answer_question
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Store retrievers per session
active_retrievers = {}

def process_profile(linkedin_url, api_key, use_mock):
    try:
        if use_mock and not linkedin_url:
            linkedin_url = "https://www.linkedin.com/in/dummy/"

        profile_data = extract_linkedin_profile(
            linkedin_url,
            api_key if not use_mock else None,
            mock=use_mock
        )

        if not profile_data:
            return "Failed to retrieve profile data", None

        chunks = split_profile_data(profile_data)
        retriever = create_retriever(chunks)

        facts = generate_initial_facts(retriever)

        session_id = str(uuid.uuid4())
        active_retrievers[session_id] = retriever

        return facts, session_id

    except Exception as e:
        logger.error(e)
        return f"Error: {e}", None

def chat_with_profile(session_id, user_query, chat_history):
    if not session_id or session_id not in active_retrievers:
        return chat_history + [
            {"role": "assistant", "content": "Please process a profile first."}
        ]

    if not user_query.strip():
        return chat_history

    retriever = active_retrievers[session_id]
    answer = answer_question(retriever, user_query)

    return chat_history + [
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": answer}
    ]

def create_gradio_interface():
    with gr.Blocks(title="LinkedIn Icebreaker Bot") as demo:
        gr.Markdown("# LinkedIn Icebreaker Bot")

        with gr.Tab("Process Profile"):
            linkedin_url = gr.Textbox(label="LinkedIn URL")
            api_key = gr.Textbox(label="ProxyCurl API Key", type="password")
            use_mock = gr.Checkbox(label="Use Mock Data", value=True)

            process_btn = gr.Button("Process")

            result = gr.Textbox(lines=10, label="Initial Facts")
            session_id = gr.Textbox(visible=False)

            process_btn.click(
                process_profile,
                inputs=[linkedin_url, api_key, use_mock],
                outputs=[result, session_id]
            )

        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(height=400)
            query = gr.Textbox(label="Ask a question")
            send = gr.Button("Send")

            send.click(
                chat_with_profile,
                inputs=[session_id, query, chatbot],
                outputs=[chatbot]
            )

            query.submit(
                chat_with_profile,
                inputs=[session_id, query, chatbot],
                outputs=[chatbot]
            )

    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(server_name="127.0.0.1", server_port=5000, share=True)
