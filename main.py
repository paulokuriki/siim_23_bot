#https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/

import json
import os

import requests
from flask import Flask, request, Response

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
                                       {"text": "Check Status", "callback_data": "check_status"}])
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


# Reading the JSON format when we send the text message and extracting the chat id of the user and the text that user send to the bot
def tel_parse_message(message):
    print("message-->", message)
    try:

        if message.get('message', None):
            chat_id = message['message']['chat']['id']
            txt = message['message']['text']
            username = message['message']['from']['username']
        elif message.get('callback_query', None):
            chat_id = message['callback_query']['from']['id']
            txt = message['callback_query']['data']
            username = message['callback_query']['from']['username']
        else:
            return '', '', ''

        print("chat_id-->", chat_id)
        print("txt-->", txt)
        print("username-->", username)

        return chat_id, txt, username
    except:
        print("No text found-->>")


# Get the Text message response from the bot
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=payload)
    return r


# Get the Image response from the bot by providing the image link
def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg"
    }
    r = requests.post(url, json=payload)
    return r


# Get the Poll response from the bot
def tel_send_poll(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPoll'
    payload = {
        'chat_id': chat_id,
        "question": "In which direction does the sun rise?",
        # options are provided in json format
        "options": json.dumps(["North", "South", "East", "West"]),
        "is_anonymous": False,
        "type": "quiz",
        # Here we are providing the index for the correct option(i.e. indexing starts from 0)
        "correct_option_id": 2
    }
    r = requests.post(url, json=payload)
    return r


# Get the Button response in the keyboard section
def tel_send_button(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "What is this?",  # button should be in the propper format as described
        'reply_markup': {
            'keyboard': [[
                {
                    'text': 'supa'
                },
                {
                    'text': 'mario'
                }
            ]]
        }
    }
    r = requests.post(url, json=payload)
    return r


# Get the Inline button response
def tel_send_inlinebutton(chat_id, message, options):
    '''

    :param chat_id: parameter received from Telegram
    :param message: Header message
    :param options: eg [{"text": "A", "callback_data": "ic_A"}, {"text": "B", "callback_data": "ic_B"}]
    :return: the request response
    '''

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': message,
        'reply_markup': {"inline_keyboard": [options]}
    }
    r = requests.post(url, json=payload)
    return r


# Get the Button response from the bot with the redirected URL
def tel_send_inlineurl(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "Which link would you like to visit?",
        'reply_markup': {
            "inline_keyboard": [
                [
                    {"text": "google", "url": "http://www.google.com/"},
                    {"text": "youtube", "url": "http://www.youtube.com/"}
                ]
            ]
        }
    }
    r = requests.post(url, json=payload)
    return r


# Get the Audio response from the bot by providing the URL for the audio
def tel_send_audio(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAudio'

    payload = {
        'chat_id': chat_id,
        "audio": "http://www.largesound.com/ashborytour/sound/brobob.mp3",
    }
    r = requests.post(url, json=payload)
    return r


# Get the Document response from the bot by providing the URL for the Document
def tel_send_document(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'

    payload = {
        'chat_id': chat_id,
        "document": "http://www.africau.edu/images/default/sample.pdf",
    }
    r = requests.post(url, json=payload)
    return r


if __name__ == '__main__':
    app.run(threaded=True)
