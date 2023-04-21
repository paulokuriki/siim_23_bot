# https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/

# import necessary modules
from flask import Flask, request, Response

from messages import *
# import functions from other modules
from telegram_aux import *

# create Flask app object
app = Flask(__name__)


# route for the root directory; handles Telegram messages
@app.route('/', methods=['GET', 'POST'])
def index():
    # Declare dict_users_hp as a global variable to modify it within the function
    if request.method == 'POST':

        # get the message from the POST request
        msg = request.get_json()

        # try:
        # parse the message to a structured dictionary
        dict_msg = tel_parse_message(msg)

        user_id = dict_msg.get('user_id', '')
        txt = dict_msg.get('txt', '')

        # load dict from disk, update it and save it back to disk
        dict_user_hp = db.load_dict(user_id)
        dict_user_hp = update_dict_user_hps(dict_user_hp, dict_msg)
        db.save_dict(dict_user_hp, user_id)

        # TODO remove before deploying in production
        # tel_send_message(chat_id, json.dumps(dict_user_hp, indent=2))

        # register the competitor in the database, if necessary
        if not db.list_competitors(dict_msg):
            db.insert_competitor(dict_msg)

        # evaluate the user's message and respond accordingly
        if txt in 'new_model':
            dict_user_hp = {}
            db.save_dict(dict_user_hp, user_id)
            select_batch_size(dict_msg)

        elif txt in hp.batch_sizes:
            select_epochs(dict_msg)

        elif txt in hp.epochs:
            select_lr(dict_msg)

        elif txt in hp.learning_rates:
            select_batch_norm(dict_msg)

        elif txt in hp.batch_norm:
            select_filters(dict_msg)

        elif txt in hp.filters:
            select_dropout(dict_msg)

        elif txt in hp.dropout:
            select_image_size(dict_msg)

        elif txt in hp.image_size:
            confirm_training(dict_msg, dict_user_hp)

        elif txt == "submit_training":
            submit_model(dict_msg, dict_user_hp)

        elif txt == "list_competitors":
            results = json.dumps(db.list_competitors(), indent=2, default=str)
            msg = 'Users:\n' + results
            tel_send_message(dict_msg, msg)

        elif txt == "show_leaderboard":
            show_leaderboard(dict_msg)

        elif txt == "show_status":
            show_training_status(dict_msg)
        else:
            dict_user_hp = {}
            db.save_dict(dict_user_hp, user_id)
            welcome_message(dict_msg)

        # except Exception as e:
        #    print(e)

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
@app.route('/notify_results', methods=['GET'])
def notify_results():
    # Notify the competitors
    results = notify_finished_trainings()

    # Return the number of users notified
    return f'{str(results)} users notified.'


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
