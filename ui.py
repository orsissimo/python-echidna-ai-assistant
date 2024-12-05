import gradio as gr
import time
from slither import run_slither_analysis
from echidna import run_echidna_test
from utils import load_prompt, parse_input, call_claude

# Load system prompts
prompt_generate_test = load_prompt('prompt_generate_test.txt')
prompt_guideline = load_prompt('prompt_guideline.txt')

def create_ui(client, output_dir):
    def chatbot(user_input, history=[]):
        history = history or []

        # Input Parsing
        user_contract_code = parse_input(user_input)
        time.sleep(1)
        history.append({'role': 'assistant', 'content': "✅ **Input Parsing Completed.**"})
        yield history

        # Static Analysis (Slither)
        slither_output = run_slither_analysis(user_contract_code, output_dir)
        time.sleep(1)
        history.append({'role': 'assistant', 'content': f"### 🔍 Slither Analysis Findings:\n{slither_output}"})
        yield history

        # TODO: Automatically fix contract errors found by Slither

        # Use case Generation (AI)
        echidna_guideline_response = call_claude(
            client,
            prompt_guideline,
            f"Slither Output:\n{slither_output}\n\nContract:\n{user_contract_code}"
        )
        time.sleep(1)
        history.append({'role': 'assistant', 'content': f"### 🫧 Generated Use Case:\n{echidna_guideline_response}"})
        yield history

        # Echidna Test Generation (AI)
        echidna_test_response = call_claude(
            client,
            prompt_generate_test,
            f"Use case:\n{echidna_guideline_response}\n\nContract:\n{user_contract_code}"
        )
        time.sleep(1)
        history.append({'role': 'assistant', 'content': f"### 🛠️ Generated Echidna Tests:\n{echidna_test_response}"})
        yield history

        # Dynamic Analysis (Echidna)
        echidna_output = run_echidna_test(user_contract_code, echidna_test_response, output_dir)
        time.sleep(1)
        history.append({'role': 'assistant', 'content': f"### 🚀 Echidna Testing Output:\n{echidna_output}"})
        yield history

        # TODO: If AI generates bad Echidna code, regenerate it and run Echidna again
        # TODO: Automatically fix contract errors found by Echidna

        # Done
        history.append({'role': 'assistant', 'content': "✅ **Done!**"})
        yield history

    def user(message, history):
        history = history or []
        history.append({'role': 'user', 'content': message})
        return "", history

    def bot(history):
        user_input = history[-1]['content']
        chatbot_generator = chatbot(user_input, history[:-1])
        for updated_history in chatbot_generator:
            time.sleep(1)
            yield updated_history

    theme = gr.themes.Monochrome()
    
    with gr.Blocks(theme=theme, css="""
        .gradio-container {height: 100vh; width: 100vw;}
        #chatbox {height: calc(100vh - 150px); overflow:auto;}
        #input_row {align-items: center; display: flex; width: 100%; padding-top: 10px;}
        #message_input {flex-grow: 5;}
        #send_button {flex-grow: 1; max-width: 15%;}
        """) as demo:
        
        gr.Markdown("<h1 style='text-align: center;'>Solidity Vulnerabilities AI Assistant 🦄 <a href='https://github.com/orsissimo'>@orsissimo</a></h1>")
        chatbot_ui = gr.Chatbot(elem_id="chatbox", type='messages')

        with gr.Row(elem_id="input_row"):
            msg = gr.Textbox(
                placeholder="Paste your smart contract code here...",
                label="",
                show_label=False,
                container=False,
                lines=10,
                elem_id="message_input"
            )
            send_button = gr.Button("Analyze", elem_id="send_button")

        clear = gr.Button("Clear chat")

        send_button.click(user, [msg, chatbot_ui], [msg, chatbot_ui], queue=False).then(
            bot, chatbot_ui, chatbot_ui, queue=True
        )
        msg.submit(user, [msg, chatbot_ui], [msg, chatbot_ui], queue=False).then(
            bot, chatbot_ui, chatbot_ui, queue=True
        )
        clear.click(lambda: [], None, chatbot_ui, queue=False)

    return demo