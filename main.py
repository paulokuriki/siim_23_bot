#https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/

from flask import Flask, request, Response

from telegram_aux import *
from database import *

# token that we get from the BotFather
TOKEN = os.environ.get('TELEGRAM_TOKEN', '')

app = Flask(__name__)

# Reading the response from the user and responding to it accordingly
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt, username = tel_parse_message(msg)
            if txt.lower() == "hi":
                tel_send_message(chat_id, f"Hello, {username}! Welcome to the SIIM 2023 AI Playground")
                tel_send_inlinebutton(chat_id, "Select your option:",
                                      [{"text": "Create new model", "callback_data": "new_model"},
                                       {"text": "Check Status", "callback_data": "check_status"},
                                       {"text": "List Users", "callback_data": "list_users"}])
            elif txt == "new_model":
                tel_send_message(chat_id, f"Creating a new model for user {username}.")
                tel_send_inlinebutton(chat_id, "Select your architecture:",
                                      [{"text": "EfficientNet", "callback_data": "efficient_net"},
                                       {"text": "ResNet", "callback_data": "res_net"}])
            elif txt in ['efficient_net', 'res_net']:
                tel_send_message(chat_id, f"Model selected: {txt}.")
                tel_send_inlinebutton(chat_id, "Select the number of epochs:",
                                      [{"text": "1", "callback_data": "1_epoch"},
                                       {"text": "3", "callback_data": "3_epochs"},
                                       {"text": "10", "callback_data": "10_epochs"}])
            elif txt in ['1_epoch', '3_epochs', '10_epochs']:
                tel_send_message(chat_id, f"Training your model for: {txt}.")
            elif txt == "check_status":
                tel_send_message(chat_id, f"{username}, here is your model's status: Train Loss: 6.3  Val Loss: 8.6 ROC AUC: 0.89")
            elif txt == "list_users":
                tel_send_message(chat_id, list_users())
            elif txt == "image":
                tel_send_image(chat_id)
            elif txt == "poll":
                tel_send_poll(chat_id)
            elif txt == "button":
                tel_send_button(chat_id)
            elif txt == "audio":
                tel_send_audio(chat_id)
            elif txt == "file":
                tel_send_document(chat_id)
            elif txt == "inlineurl":
                tel_send_inlineurl(chat_id)
            elif txt == "ic_A":
                tel_send_message(chat_id, "You have clicked A")
            elif txt == "ic_B":
                tel_send_message(chat_id, "You have clicked B")
            else:
                tel_send_message(chat_id,
                                 'Hi Felipe and Tim. Welcome to the AI Playground.\n'
                                 'Say HI to start.')
        except:
            print("fromindex-->")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"




if __name__ == '__main__':
    app.run(threaded=True)
