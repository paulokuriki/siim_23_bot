import json
import os

import requests

# token that we get from the BotFather
TOKEN = os.environ.get('TELEGRAM_TOKEN', '')


# Reading the JSON format when we send the text message and extracting the chat id of the user and the text that user send to the bot
def tel_parse_message(message):
    print("message-->", message)
    try:

        chat_id = txt = user_id = username = firstname = lastname = fullname = ''

        if message.get('message', None):
            chat_id = message.get('message', {}).get('chat', {}).get('id', '')
            txt = message.get('message', {}).get('text', '')
            user_id = str(message.get('message', {}).get('from', {}).get('id', ''))
            username = message.get('message', {}).get('from', {}).get('username', '')
            firstname = message.get('message', {}).get('from', {}).get('first_name', '')
            lastname = message.get('message', {}).get('from', {}).get('last_name', '')
            fullname = f'{firstname} {lastname}'
        elif message.get('callback_query', None):
            chat_id = message.get('callback_query', {}).get('from', {}).get('id', '')
            txt = message.get('callback_query', {}).get('data', '')
            user_id = str(message.get('callback_query', {}).get('from', {}).get('id', ''))
            username = message.get('callback_query', {}).get('from', {}).get('username', '')
            firstname = message.get('callback_query', {}).get('from', {}).get('first_name', '')
            lastname = message.get('callback_query', {}).get('from', {}).get('last_name', '')
            fullname = f'{firstname} {lastname}'

        return {'chat_id': chat_id,
                'txt': txt,
                'user_id': user_id,
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'fullname': fullname
                }
    except:
        print("No text found-->>")


# Get the Text message response from the bot
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'parse_mode': 'Markdown',
        'text': text
    }
    r = requests.post(url, json=payload)
    return r


# Get the Image response from the bot by providing the image link
def tel_send_image(chat_id, img_url):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': img_url
    }
    print(payload)
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
        'parse_mode': 'Markdown',
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


def tel_get_user_photos(user_id, offset=0, limit=1):
    url = f'https://api.telegram.org/bot{TOKEN}/getUserProfilePhotos'
    payload = {
        'user_id': user_id,
        'offset': offset,
        'limit': limit
    }
    r = requests.post(url, json=payload)
    return r

def tel_download_file(file_id, file_unique_id):
    url = f'https://api.telegram.org/file/bot<TOKEN>'

    payload = {
        'file_id': file_id,
        'file_unique_id': file_unique_id,
    }
    r = requests.post(url, json=payload)
    return r