# https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/

from flask import Flask, request, Response

from telegram_aux import *
from messages import *
import database as db
import hyperparameters as hp

app = Flask(__name__)


# Reading the response from the user and responding to it accordingly
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt, username, fullname = tel_parse_message(msg)

            # register the competitor in the database, if necessary
            if not db.list_competitors(username=username):
                db.insert_competitor(username=username, fullname=fullname)

            # evaluate the user's message
            if txt == "hi":
                welcome_message(chat_id, txt, username, fullname)

            elif txt in 'new_model':
                select_batch_size(chat_id, txt, username, fullname)

            elif txt in hp.batch_sizes:
                select_epochs(chat_id, txt, username, fullname)

            elif txt in hp.epochs:
                select_lr(chat_id, txt, username, fullname)

            elif txt in hp.learning_rates:
                select_batch_norm(chat_id, txt, username, fullname)

            elif txt in hp.batch_norm:
                select_filters(chat_id, txt, username, fullname)

            elif txt in hp.filters:
                select_dropout(chat_id, txt, username, fullname)

            elif txt in hp.dropout:
                select_image_size(chat_id, txt, username, fullname)

            elif txt in hp.image_size:
                confirm_training(chat_id, txt, username, fullname)

            elif txt in hp.image_size:
                confirm_training(chat_id, txt, username, fullname)

            elif txt == "submit_training":
                submit_model(chat_id, txt, username, fullname)

            elif txt == "list_competitors":
                msg = 'Users:\n' + '\n'.join(db.list_competitors())
                tel_send_message(chat_id, msg)

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
                welcome_message(chat_id, txt, username, fullname)

        except:
            print("fromindex-->")

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    app.run(threaded=True)
