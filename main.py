import gradio as gr
import time
import pandas as pd

dataset = pd.read_excel("dataset.xlsx")
alphabet = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"


def convert_to_no(cell):
    cell = cell.lower()
    cell_no = [int(cell[1:])-2, alphabet.index(cell[0])]
    return cell_no


def convert_to_xl(cell_no):
    cell = alphabet[cell_no[1]].upper()+str(cell_no[0]+2)
    return cell


def convert_to_dict(response, cell_no):
    response = response.to_dict()
    response_tmp = response.copy()
    for key in response_tmp.keys():
        response[convert_to_xl([key, cell_no[1]+1])
                 ] = response.pop(key, None)
    return response

def gen_response(cell):
    cell_no = convert_to_no(cell)
    if (cell == "A1"):
        cell="A2"
        cell_no = convert_to_no(cell)
        response = dataset.iloc[cell_no[0]:len(dataset.index), cell_no[1]+1].dropna()
        response = response.to_dict()
        response_tmp = response.copy()
        for key in response_tmp.keys():
            response[convert_to_xl([key, cell_no[1]])
                     ] = response.pop(key, None)
        print(response)
        # return response
        tmp = ""
        for x in response:
            tmp+=f"{x}: {response[x]}\n"
        return tmp

    if (cell_no[1]%2 == 0):
        # response = dataset.iloc[cell_no[0], cell_no[1]+1]
        # response = {convert_to_xl([cell_no[0], cell_no[1]+1]): response}
        response = {"Question": dataset.iloc[cell_no[0], cell_no[1]+1]}
        next = dataset.index.where(dataset[list(dataset.columns)[cell_no[1]+1]].notna().dropna())
        next = list(i for i in (list(next)) if i>cell_no[0])[0]
        options = dataset.iloc[cell_no[0]:int(next), cell_no[1]+2].dropna()
        options = convert_to_dict(options, [cell_no[0], cell_no[1]+1])
        response["Options"]=options
        # return response
        tmp = f"Question: {response['Question']}\nResponses:\n"
        for x in response["Options"].keys():
            tmp += f"{x}: {response['Options'][x]}\n"
        return tmp


with gr.Blocks() as demo:
    global history
    history = (
        "-----------------------------------------------------------------------\n")

    msg = gr.Textbox(label="User Input")
    chatbot = gr.Chatbot()

    clear = gr.ClearButton([msg, chatbot])

    def respond(user_message, chat_history):
        global history
        history += f"User: {user_message}\nChatbot: "

        bot_message = gen_response(user_message)
        history += f"{bot_message}\n"

        chat_history.append([user_message, bot_message])
        time.sleep(0.5)
        print(history)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])


demo.launch()
