import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Request

import database as db
import db_schema
import hyperparameters as hp
from telegram_aux import tel_send_message, tel_send_inlinebutton, tel_send_image


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

    tel_send_message(chat_id, "Let's train your new model.")
    tel_send_message(chat_id, "A Machine Learning model is trained over many images.\n"
                              "It's also important to select some parameters that can improve your model's performance\n"
                              "In the next steps, you will select some of these parameters.")
    tel_send_message(chat_id, "First, you have to select a batch size.")
    tel_send_message(chat_id,
                     "[Learn more](https://radiopaedia.org/articles/batch-size-machine-learning)")
    tel_send_inlinebutton(chat_id, "*Select the Batch Size:*", create_dict_options(hp.batch_sizes))


# Sends options for selecting number of epochs to the user
def select_epochs(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, f"Now, select the number of epochs to be trained.")
    tel_send_message(chat_id, "[Learn more](https://radiopaedia.org/articles/epoch-machine-learning)")
    tel_send_inlinebutton(chat_id, "*Select the Number of Epochs:*", create_dict_options(hp.epochs))


# Sends options for selecting learning rate to the user
def select_lr(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "Great, now let's select the learning rate.")
    tel_send_message(chat_id,
                     "[Learn more](https://radiopaedia.org/articles/optimization-algorithms)")
    tel_send_inlinebutton(chat_id, "*Select the Learning Rate*:", create_dict_options(hp.learning_rates))


# Sends options for selecting whether or not to use batch normalization to the user
def select_batch_norm(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, f"It's time to decide if you want to use batch normalization.")
    tel_send_message(chat_id,
                     "[Learn more](https://radiopaedia.org/articles/normalization-general)")
    tel_send_inlinebutton(chat_id, "*Select the Batch Norm*:", create_dict_options(hp.batch_norm))


# Sends options for selecting number of filters to the user
def select_filters(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "Awesome. Now, a important hyperparameter: the number of filters.")
    tel_send_message(chat_id,
                     "[Learn more](https://radiopaedia.org/articles/kernel-image-processing)")
    tel_send_inlinebutton(chat_id, "*Select the Number of Filters:*", create_dict_options(hp.filters))


# Sends options for selecting whether or not to use dropout to the user
def select_dropout(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, f"Optionally, you can opt to apply dropout to your model.")
    tel_send_message(chat_id,
                     "[Learn more](https://machinelearningmastery.com/dropout-for-regularizing-deep-neural-networks/)")
    tel_send_inlinebutton(chat_id, "*Use Dropout:*", create_dict_options(hp.dropout))


# Sends options for selecting image size to the user
def select_image_size(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "For last, but not the least, select the image size to input in your model.")
    tel_send_message(chat_id,
                     "[Learn more](https://radiopaedia.org/articles/scaling)")
    tel_send_inlinebutton(chat_id, "*Select the Image Size:*", create_dict_options(hp.image_size))


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
        tel_send_message(chat_id, f"The estimated training time is {convert_seconds(estimated_time)}")
        tel_send_message(chat_id, "You'll receive an automatic message when your training is finished.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Check Status", "callback_data": "show_status"},
                               {"text": "Cancel Training", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])
    else:
        tel_send_message(chat_id, "There was a problem submitting your model to the training queue. "
                                  "Try again in a few minutes. "
                                  "If the problem persists, notify the SIIM AI Playground organizers.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Try new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])


def show_training_status(dict_msg: dict = {}, request: Request = None):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    # Loads user's submissions
    df = db.load_df_submissions(user_id)

    if len(df) == 0:
        # If there is no submission
        tel_send_message(chat_id, "You didn't submit any model to training yet.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Create new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])
    else:
        # Submission were found
        rec = df.loc[0]

        if rec.training_status in db_schema.TRAINING_STATUS_TRAINING:
            # The last submission is training

            estimated_time = calc_timestamp_diff_in_secs(str(rec.datetime_submission),
                                                         str(rec.datetime_results_available))

            time_remaining = calc_timestamp_diff_in_secs(str(datetime.datetime.now()),
                                                         str(rec.datetime_results_available))

            # checks if it is finished
            if time_remaining > 0:
                # the training session period is not over yet. the competitor has to wait
                tel_send_message(chat_id, "*TRAINING STATUS:*\n"
                                          f"Estimated training time: {convert_seconds(estimated_time)}\n"
                                          f"Time remaining: {convert_seconds(time_remaining)}")
                tel_send_message(chat_id, "You'll receive an automatic message when your training is finished.")
                tel_send_inlinebutton(chat_id, "Select your option:",
                                      [{"text": "Check Status", "callback_data": "show_status"},
                                       {"text": "Cancel Training", "callback_data": "new_model"},
                                       {"text": "Leaderboard", "callback_data": "show_leaderboard"}])

            else:
                # The training session is over. Notify the user and change status in the database
                notify_finished_trainings(request=request, urer_id=user_id)


def show_leaderboard(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    df = db.get_leaderboard_df()

    df['last_submission'] = df['last_submission'].apply(calculate_time_ago)
    df['rank'] = df.index + 1

    # Look for the user_id in the dataframe
    df_user = df[df['user_id'] == user_id]

    df = df[['rank', 'fullname', 'score', 'entries', 'last_submission']]
    df.columns = ['Pos', 'Name', 'Score', 'Entries', 'Last']
    leaderboard = df.to_string(index=False)

    if not df_user.empty:
        # Find the position (index) of the first matching row and add 1 to start counting from 1
        position = int(df_user.index[0] + 1)

        # Create a series called rec of the first matching row
        row = df_user.iloc[0]

        tel_send_message(chat_id,
                         f"Your are in the *{number_to_ordinal(position)}* position. Your best score is *{row.score}*")
        tel_send_message(chat_id, "*LEADERBOARD (Top 10)*")
        tel_send_message(chat_id, '```' + leaderboard + '```')
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Try new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])


    else:
        # User not found in the dataframe.
        tel_send_message(chat_id, "*LEADERBOARD*")
        tel_send_message(chat_id, f"You have not ranked yet. Create a new model or wait your model to finish training.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Check Status", "callback_data": "show_status"},
                               {"text": "Create new model", "callback_data": "new_model"}])

    return


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

    # Remove _ to avoid formatting issues (italic)
    txt = txt.replace('_', ' ')

    return txt


def calc_timestamp_diff_in_secs(timestamp1, timestamp2):
    # Convert the strings to datetime objects using strptime()
    # Adjust the format string if your input has a different format
    print(timestamp1, timestamp2)
    dt1 = datetime.datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f")
    dt2 = datetime.datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f")

    # Calculate the time difference and convert it to seconds
    time_difference = dt2 - dt1
    time_difference_seconds = int(time_difference.total_seconds())

    return time_difference_seconds


def notify_finished_trainings(request: Request, user_id: str = None):
    df = db.load_df_finished_trainings(user_id)

    list_competitors_notified = []

    for idx, row in df.iterrows():
        if row.user_id not in list_competitors_notified:
            tel_send_message(row.chat_id, "Your model training is *FINISHED*. Here are your results:\n"
                                          f"*Training set:* {row.metrics_train_set}\n"
                                          f"*Validation set:* {row.metrics_val_set}\n"
                                          f"*Test set:* {row.metrics_test_set}")

            dice, jacloss, sample = db_schema.imgs_url(0, row.epochs, row.learning_rate, row.batch_norm, row.filters,
                                                       row.dropout, row.image_size, row.batch_size)

            # rotates the sample image as they as originally they were created rotated
            sample = request.url_for("rotate_image", image_url=sample)

            tel_send_image(row.chat_id, dice)
            tel_send_image(row.chat_id, jacloss)
            tel_send_image(row.chat_id, sample)

            tel_send_inlinebutton(row.chat_id, "Select your option:",
                                  [{"text": "Leaderboard", "callback_data": "show_leaderboard"},
                                   {"text": "Try new model", "callback_data": "new_model"}])

            list_competitors_notified.append(row.user_id)

    db.mark_submissions_notified(list_competitors_notified)

    return len(list_competitors_notified)


def convert_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"


def calculate_time_ago(timestamp: str):
    # Parse the input timestamp string
    timestamp = str(timestamp)
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

    # Calculate the difference between now and the input timestamp
    now = datetime.datetime.now()
    time_difference = now - timestamp
    relative_difference = relativedelta(now, timestamp)

    # Check if the difference is less than one minute
    if time_difference < datetime.timedelta(minutes=1):
        return 'Now'

    # Check if the difference is more than a year
    elif relative_difference.years >= 1:
        years = relative_difference.years
        return f'{years}y'

    # Check if the difference is more than a month but less than a year
    elif relative_difference.months >= 1:
        months = relative_difference.months + relative_difference.years * 12
        return f'{months}mo'

    # Check if the difference is more than a day
    elif time_difference >= datetime.timedelta(days=1):
        days = time_difference.days
        return f'{days}d'

    # Check if the difference is more than an hour but less than a day
    elif time_difference >= datetime.timedelta(hours=1):
        hours = time_difference.seconds // 3600
        return f'{hours}h'

    # If the difference is less than a day but more than a minute
    else:
        minutes = time_difference.seconds // 60
        return f'{minutes}min'


def number_to_ordinal(n):
    if isinstance(n, (int, float)):
        n = int(n)
    else:
        raise TypeError("The input should be a number.")

    if n < 0:
        raise ValueError("The input should be a non-negative integer.")

    if n % 100 in [11, 12, 13]:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

    return str(n) + suffix


def read_html_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        content = f.read()
    return content
