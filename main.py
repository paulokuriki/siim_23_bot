# https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/

# import necessary modules
from flask import Flask, request, Response

# import functions from other modules
from telegram_aux import *
from messages import *
import database as db
import hyperparameters as hp

# create Flask app object
app = Flask(__name__)


# route for the root directory; handles Telegram messages
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get the message from the POST request
        msg = request.get_json()
        try:
            # parse the message using functions from telegram_aux.py
            chat_id, txt, user_id, username, fullname = tel_parse_message(msg)

            # register the competitor in the database, if necessary
            if not db.list_competitors(user_id=user_id):
                db.insert_competitor(user_id=user_id, username=username, fullname=fullname)

            # evaluate the user's message and respond accordingly
            if txt == "hi":
                welcome_message(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in 'new_model':
                select_batch_size(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.batch_sizes:
                select_epochs(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.epochs:
                select_lr(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.learning_rates:
                select_batch_norm(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.batch_norm:
                select_filters(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.filters:
                select_dropout(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.dropout:
                select_image_size(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.image_size:
                confirm_training(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt in hp.image_size:
                confirm_training(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt == "submit_training":
                submit_model(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt == "list_competitors":
                msg = 'Users:\n' + '\n'.join(db.list_competitors())
                tel_send_message(chat_id, msg)

            elif txt == "show_leaderboard":
                show_leaderboard(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

            elif txt == "show_status":
                show_training_status(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

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
                welcome_message(chat_id=chat_id, txt=txt, user_id=user_id, username=username, fullname=fullname)

        except Exception as e:
            print(e)

        return Response('ok', status=200)
    else:
        return "<h1>Welcome to the SIIM AI Playground API!</h1>" \
               "<p>Open Telegram and look for the bot called @siim_23_bot to start to play."


# route for uploading JSON records to the database
@app.route('/upload_json', methods=['POST'])
def upload_json():
    if request.method == 'POST':
        try:
            # get the JSON record from the POST request
            json_record = request.get_json()
            # insert the record into the database using a function from database.py
            result = db.insert_json(json_record)
            # return an appropriate response based on the result of the insertion
            if result == 'JSON inserted successfully.':
                return result, 200
            else:
                return result, 500

        except Exception as e:
            # return an error response if the insertion fails
            return e, 500


# route for listing pretrained model metrics
@app.route('/list_pretrained_metrics', methods=['GET'])
def list_pretrained_metrics():
    # get the pretrained metrics from the database using a function from database.py
    results = json.dumps(db.list_pretrained(), indent=2, default=str)
    # return the results as a JSON object
    return results


# route for listing pretrained model metrics
@app.route('/list_competitors', methods=['GET'])
def list_competitors():
    # get the pretrained metrics from the database using a function from database.py
    results = json.dumps(db.list_competitors(), indent=2, default=str)
    # return the results as a JSON object
    return results


# start the Flask app if this file is being run as the main program
if __name__ == '__main__':
    app.run(threaded=True)
