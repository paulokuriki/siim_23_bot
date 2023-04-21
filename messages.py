import datetime

import database as db
import hyperparameters as hp
from telegram_aux import tel_send_message, tel_send_inlinebutton


def update_dict_user_hps(dict_user_hp: dict = {}, dict_msg: dict = {}) -> dict:
    # Get the user_id and txt fields from the dict_msg dictionary, providing default values if the keys are not found
    txt = dict_msg.get('txt', '')

    # Call the extract_dict_options function to parse the txt field into a key-value pair
    key, value = extract_dict_options(txt)

    # If key and value variables have 'values'
    if key != '' and value != '':
        # Update the user's dictionary with the new key-value pair
        dict_user_hp[key] = value

    # Return the updated main dictionary (dict_users_hp)
    return dict_user_hp


# Sends a welcome message to the user and provides options for training a new model or checking status
def welcome_message(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, f"Hello, {fullname}! Welcome to the SIIM 2023 AI Playground")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "Train new model", "callback_data": "new_model"},
                           {"text": "Check Status", "callback_data": "show_status"}])


# Sends options for selecting batch size to the user
def select_batch_size(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "Let's train your new model. It's time to have fun.")
    tel_send_message(chat_id, "First, you have to select a batch size.")
    tel_send_inlinebutton(chat_id, "Batch Size:", create_dict_options(hp.batch_sizes))


# Sends options for selecting number of epochs to the user
def select_epochs(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, f"Now, select the number of epochs to be trained.")
    tel_send_inlinebutton(chat_id, "Epochs:", create_dict_options(hp.epochs))


# Sends options for selecting learning rate to the user
def select_lr(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "Great, now let's select the learning rate.")
    tel_send_inlinebutton(chat_id, "Learning Rates:", create_dict_options(hp.learning_rates))


# Sends options for selecting whether or not to use batch normalization to the user
def select_batch_norm(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, f"It's time to decide if you want to use batch normalization.")
    tel_send_inlinebutton(chat_id, "Batch Norm:", create_dict_options(hp.batch_norm))


# Sends options for selecting number of filters to the user
def select_filters(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "Awesome. Now, a important hyperparameter: the number of filters.")
    tel_send_inlinebutton(chat_id, "Number of Filters:", create_dict_options(hp.filters))


# Sends options for selecting whether or not to use dropout to the user
def select_dropout(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, f"Optionally, you can opt to apply dropout to your model.")
    tel_send_inlinebutton(chat_id, "Dropout:", create_dict_options(hp.dropout))


# Sends options for selecting image size to the user
def select_image_size(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "For last, but not the least, select the image size to input in your model.")
    tel_send_inlinebutton(chat_id, "Image Size:", create_dict_options(hp.image_size))


def confirm_training(dict_msg: dict = {}, dict_user_hp: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    fullname = dict_msg.get('fullname', '')

    txt_user_hps = parse_user_hps(dict_user_hp)

    tel_send_message(chat_id, f"Nice work, {fullname}! ")
    tel_send_message(chat_id, f"Here are your selected hyperparameters:{txt_user_hps}")
    tel_send_message(chat_id, "If you are happy with the selected hyperparameters, click on the [Train] button below.")
    tel_send_message(chat_id, "If you want to cancel and define a new model, click on the [Cancel] button.")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "Train", "callback_data": "submit_training"},
                           {"text": "Cancel", "callback_data": "new_model"}])


def submit_model(dict_msg: dict = {}, dict_user_hp: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    # estimated_time = db.make_submission(dict_user_hp, user_id, random_estimated_time, random_metrics_train_set, random_metrics_val_set, random_metrics_test_set)
    estimated_time = db.make_submission(dict_user_hp, user_id, chat_id)

    if estimated_time > 0:
        tel_send_message(chat_id, "Your model was submitted to the training queue.")
        tel_send_message(chat_id, f"The estimated training time is {estimated_time} secs")
        tel_send_message(chat_id, "You'll receive a message when your training model is finish.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Check Status", "callback_data": "show_status"},
                               {"text": "Cancel Training", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])
    else:
        tel_send_message(chat_id, "There was a problem submitting your model to the training queue. "
                                  "Try again in a few minutes. "
                                  "If the problem persists, notify the SIIM AI Playground organizers.")


def show_training_status(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    df = db.load_df_submissions(user_id)

    if len(df) == 0:
        tel_send_message(chat_id, "You didn't submit any model to training yet.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Create new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])
    else:
        rec = df.loc[0]

        estimated_time = calc_timestamp_diff_in_secs(str(rec.datetime_submission),
                                                     str(rec.datetime_results_available))
        time_remaining = calc_timestamp_diff_in_secs(str(datetime.datetime.now()),
                                                     str(rec.datetime_results_available))

        ranking = calc_timestamp_diff_in_secs(str(datetime.datetime.now()),
                                              str(rec.datetime_results_available))

        if time_remaining <= 0:
            tel_send_message(chat_id, "RESULTS: TRAINING METRICS:")
            tel_send_message(chat_id, f"Training set: {rec.metrics_train_set}")
            tel_send_message(chat_id, f"Validation set: {rec.metrics_test_set}")
            tel_send_message(chat_id, f"Validation set: {rec.metrics_val_set}")
            tel_send_inlinebutton(chat_id, "Select your option:",
                                  [{"text": "Try new model", "callback_data": "new_model"},
                                   {"text": "Leaderboard", "callback_data": "show_leaderboard"}])

        else:

            tel_send_message(chat_id, "TRAINING STATUS:")
            tel_send_message(chat_id, f"The estimated training time is {estimated_time} secs")
            tel_send_message(chat_id, f"Time remaining: {time_remaining} secs")
            tel_send_message(chat_id,
                             "If you want to cancel the training process and define a new model, click on the CANCEL button.")
            tel_send_message(chat_id, "Otherwise, you can check the training session STATUS at any time.")
            tel_send_message(chat_id,
                             "You'll receive a message with the metrics results and your position on the leaderboard as soon as the model's training is finished.")
            tel_send_inlinebutton(chat_id, "Select your option:",
                                  [{"text": "Check Status", "callback_data": "show_status"},
                                   {"text": "Cancel Training", "callback_data": "new_model"},
                                   {"text": "Leaderboard", "callback_data": "show_leaderboard"}])


def show_leaderboard(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    position = db.get_user_ranking(user_id)

    if position > 0:
        tel_send_message(chat_id, "LEADERBOARD")
        tel_send_message(chat_id, f"Your are in the position {position}")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Try new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])
    else:
        tel_send_message(chat_id, "LEADERBOARD")
        tel_send_message(chat_id, f"You are not ranked yet. Create a new model or wait your model to finish training.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Create new model", "callback_data": "new_model"},
                               {"text": "Check Status", "callback_data": "show_status"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])


def create_dict_options(list_options):
    list_dict = []

    for option in list_options:
        text = option.split(hp.sep)[1]
        callback_data = option
        list_dict.append({"text": text, "callback_data": callback_data})

    return list_dict


def extract_dict_options(txt):
    key = ''
    value = ''

    if len(txt.split(hp.sep)) == 2:
        key = txt.split(hp.sep)[0]
        value = txt.split(hp.sep)[1]

    return key, value


def parse_user_hps(dict_user_hp: dict = {}, user_id: str = '') -> str:
    txt = ''

    for key, value in dict_user_hp.items():
        txt = '\n'.join([txt, f'{key}: {value}'])

    return txt


def calc_timestamp_diff_in_secs(timestamp1, timestamp2):
    from datetime import datetime

    # Convert the strings to datetime objects using strptime()
    # Adjust the format string if your input has a different format
    print(timestamp1, timestamp2)
    dt1 = datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f")
    dt2 = datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f")

    # Calculate the time difference and convert it to seconds
    time_difference = dt2 - dt1
    time_difference_seconds = int(time_difference.total_seconds())

    return time_difference_seconds
