import openai
import gradio as gr
import time
from config import settings

openai.api_key = settings.openai_api_key

with gr.Blocks() as demo:
    global history
    history = (
        "The following is conversation between a user and an AI Health chatbot.\n"
        + "The chatbot is helpful, creative, clever, and very friendly.\n"
        + "User: "
    )

    msg = gr.Textbox(label="User Input")
    chatbot = gr.Chatbot()

    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        global history
        history += f"{message}\nChatbot: "
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=history,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop="bye",
        )

        bot_message = response.choices[0].text.strip()

        history += f"{bot_message}\nUser: "

        chat_history.append([message, bot_message])
        time.sleep(0.5)
        print(history)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])


demo.launch()
